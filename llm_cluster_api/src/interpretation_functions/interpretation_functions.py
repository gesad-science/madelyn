import requests
from src.interpretation_functions.config import COMPREHENSION_API_URL
from src.llm.LLModel import LLModel, PromptType
from src.llm.qa_service import QAService
from enum import Enum

class Intent(Enum):
    CREATE = 'create',
    READ = 'read',
    UPDATE = 'update',
    DELETE = 'delete'

class Interpretation_module:
    def __init__(self,
                 user_msg : str,
                 model : LLModel
                 ):
        self.user_msg = user_msg
        self.model = model
        self.tokens = self.generate_tokens_classification()
        self.intent = self.get_intent()
        self.entity = self.get_entity()
        self.attributes = {}
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


    def get_intent(self) -> Intent:
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
            match(response):
                case 'CREATE':
                    return Intent.CREATE
                case 'READ':
                    return Intent.READ
                case 'UPDATE':
                    return Intent.UPDATE
                case 'DELETE':
                    return Intent.DELETE
        else:
            return None



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

            # then use the text similarity service to compare the candidates with the model response to choose the better one 
            ### not implemented yet ###

            return response

        else:
            return None


    def get_attributes(self) -> dict:
        if self.tokens:

            find_attribute = None

            for token in self.tokens:
                if find_attribute is None:
                    if token['entity'] == 'NOUN' and token['word'] != self.entity: # or if the word is a known attribute key --but not implemented yet--

                        attribute_key = token['word']
                        fragment_short_idx = self.user_msg.find(attribute_key)
                        fragment_short = self.user_msg[fragment_short_idx + len(attribute_key)]

                        find_attribute = QAService().make_call(inputs={"variables" : {"attribute_key" : attribute_key, "entity" : self.entity, "user_msg" : self.user_msg, "fragment_short" : fragment_short}}, prompt_type=PromptType.ENTITY, model=self.model)
                        find_attribute = find_attribute['response']

                        self.attributes[attribute_key] = find_attribute
                else:
                    if token['word'] == find_attribute:
                        find_attribute = None

        else:
            return None
        
    def extract_data(self):
        return {'user_msg' : self.user_msg, 'intent' : self.intent, 'entity' : self.entity, 'attributes' : self.attributes}
