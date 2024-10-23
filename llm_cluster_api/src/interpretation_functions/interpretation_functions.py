import requests
from src.interpretation_functions.config import COMPREHENSION_API_URL, LIM_API_URL
from src.llm.LLModel import LLModel, PromptType
from src.llm.qa_service import QAService
from enum import Enum

from src.db.arango_model_storage import ArangoModelStorage

import re

class Intent(Enum):
    CREATE = 'create',
    READ = 'read',
    UPDATE = 'update',
    DELETE = 'delete'

class Interpretation_module:
    def __init__(self,
                 user_msg : str,
                 model_name : str
                 ):
        storage = ArangoModelStorage(url='http://arangodb-instance:8529',username='root', password='123')
        self.user_msg = user_msg
        self.model = storage.get_model(model_name)
        self.tokens = self.generate_tokens_classification()
        self.attributes = {}
        self.intent = self.get_intent()
        self.entity = self.get_entity()
        self.get_attributes()

    def generate_tokens_classification(self):
        data = {
                "func": "TOKEN_CLASSIFICATION",
                "inputs": [
                    self.user_msg
                ]
                }
        response = requests.post(COMPREHENSION_API_URL, json=data)
        return response.json()['data']
    
    def call_lim(self, request : str, attribute_key : str, attribute_value : str):
        data= {
            'user_input': self.user_msg,
            'key' : attribute_key,
            'value' : attribute_value,
            'processed_atts' : self.attributes,
            'model_name' : self.model.name,
            'current_entity' : None,
            'current_intent' : None
        }
        match(request):
            case 'intent':
                url = LIM_API_URL + '/intent'
                response = requests.post(url, json=data)
                return response
            case 'entity':
                url = LIM_API_URL + '/entity'
                data['current_intent'] = self.intent.__str__()
                response = requests.post(url, json=data)
                return response
            case 'attribute':
                url = LIM_API_URL + '/attributes'
                data['current_intent'] = self.intent
                data['current_entity'] = self.entity
                response = requests.post(url, json=data)
                return response.json()['value']
        


    def get_intent(self):
        if self.tokens:
            '''
            candidate = None
            
            for token in self.tokens:
                if token['entity'] == 'VERB':
                    candidate = token['word']
                    break
            
            # send the first verb as a hint to the model
            '''
            response = QAService().make_call(inputs={"variables" : {'user_msg' : self.user_msg}}, prompt_type=PromptType.INTENT, model=self.model)
            response = response['response']

            # while lim is not ready, make some treatments here
            response = re.sub(r'^\s+|\s+$', '', response)
            response = response.lower()

            match(response):
                case 'create':
                    return Intent.CREATE.__str__()
                case 'read':
                    return Intent.READ.__str__()
                case 'update':
                    return Intent.UPDATE.__str__()
                case 'delete':
                    return Intent.DELETE.__str__()
                case _:
                    return Intent.CREATE.__str__()
        else:
            return Intent.CREATE.__str__()



    def get_entity(self):
        if self.tokens:
            '''
            candidate = None

            for token in self.tokens:
                if token['entity'] == 'NOUN':
                    candidate = token['word']
                    break
            
            
            # we will need some function to get the existing tables/entities, for that instance, as a list

            entities = database.get_entities()


            # and check if our nouns fits some existing entity

            database_candidate = None

            for token in self.tokens:
                if token['entity'] == 'NOUN':
                    if token['word'] in entities:
                        database_candidate = token['word']
                        break

            '''

            # by now, passing the first noun as an input for prompt
            response = QAService().make_call(inputs={"variables" : {'user_msg' : self.user_msg}}, prompt_type=PromptType.ENTITY, model=self.model)

            response = response['response']

            # while lim is not ready, make some treatments here
            print(response)
            response = self.call_lim(request='entity', attribute_key='', attribute_value=response)
            response = response.json()['value']
            print(response)

            # then use the text similarity service to compare the candidates with the model response to choose the better one 
            ### not implemented yet ###

            return response

        else:
            return None


    def get_attributes(self) -> dict:
        if self.tokens:

            find_attribute = None

            for token in self.tokens:
                print(token)
                if find_attribute is None:
                    if token['entity'] == 'NOUN' and token['word'] != self.entity: # or if the word is a known attribute key --but not implemented yet--

                        attribute_key = token['word']
                        fragment_short_idx = self.user_msg.find(attribute_key)
                        fragment_short = self.user_msg[fragment_short_idx + len(attribute_key)]

                        find_attribute = QAService().make_call(inputs={
                                                                            "variables" : {
                                                                                      "attribute_key" : attribute_key, 
                                                                                      "entity" : self.entity, 
                                                                                      "user_msg" : self.user_msg, 
                                                                                      "fragment_short" : fragment_short,
                                                                                      "user_intent" : self.intent
                                                                                      }
                                                                       }, 
                                                                       prompt_type=PromptType.ATTRIBUTE, model=self.model
                                                                )
                        find_attribute = find_attribute['response']

                        find_attribute = self.call_lim(request='attribute', attribute_key=attribute_key, attribute_value=find_attribute)
                        print(find_attribute)

                        self.attributes[attribute_key] = find_attribute
                else:
                    if token['word'] == find_attribute:
                        find_attribute = None

        else:
            return None
        
    def extract_data(self):
        return {'user_msg' : self.user_msg, 'intent' : self.intent, 'entity' : self.entity, 'attributes' : self.attributes}
