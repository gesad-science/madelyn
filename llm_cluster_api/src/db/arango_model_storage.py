from arango import ArangoClient, DocumentDeleteError, DocumentUpdateError, DocumentInsertError
from src.exceptions.business_rule_exception import BusinessRuleException
from src.llm.prompt_template import PromptTemplate
from src.utils.singleton import Singleton
from src.llm.LLModel import LLModel
from uuid import UUID

from src.consts import ARANGODB_COLLECTION_NAME, ARANGODB_DATABASE_NAME, ARANGODB_PASSWORD, ARANGODB_URL, ARANGODB_USERNAME
"""
Acourding to a fast research pyarango is not thread safe by default, so
initially im just going to init a new connection for each db interaction
"""
class ArangoModelStorage():

    def __init__(self, 
                 url : str = None ,
                 username : str = None, 
                 password : str = None, 
                 collection_name = 'madelyn_model_storage_collection',
                 db_name = 'madelyn_model_storage_database',
                 ) -> None:
            # ARANGODB_URL = ''
            # ARANGODB_USERNAME = 'root'
            # ARANGODB_PASSWORD = '123'
        # url = None
        if url is None:
            url = ARANGODB_URL
        if username is None:
            username = ARANGODB_USERNAME
        if password is None:
            password = ARANGODB_PASSWORD

        if url is None:
            raise Exception('Cant connect to arangodb since no url was provided nor ARANGODB_URL environment varible declared')
        if username is None:
            raise Exception('Cant connect to arangodb since no username was provided nor ARANGODB_USERNAME environment varible declared')
        if password is None:
            raise Exception('Cant connect to arangodb since no password was provided nor ARANGODB_PASSWORD environment varible declared')

        if ARANGODB_COLLECTION_NAME is not None:
            collection_name = ARANGODB_COLLECTION_NAME

        if ARANGODB_DATABASE_NAME is not None:
            db_name = ARANGODB_DATABASE_NAME

        self.db = ArangoClient(hosts=url).db(db_name, password=password, username=username)

        if self.db.has_collection(collection_name):
            self.collection = self.db.collection(collection_name)
        else:
            self.collection = self.db.create_collection(collection_name)

        self.db_name = db_name
        self.collection_name = collection_name

    @staticmethod
    def __arango_doc_to_PromptTemplate(arango_doc : dict) -> PromptTemplate: 
        return PromptTemplate(
            template= arango_doc["template"],
            args= arango_doc["args"],
            id= UUID(arango_doc["id"])
        )

    @staticmethod
    def __arango_doc_to_LLModel(arango_doc : dict) -> LLModel:
        return LLModel(
            name = arango_doc["_key"],
            default_prompt=  ArangoModelStorage.__arango_doc_to_PromptTemplate(arango_doc["main_prompt"]),
            prompt_alternatives=[ ArangoModelStorage.__arango_doc_to_PromptTemplate(p) 
                                  for p in arango_doc["prompt_alternatives"]],
            validations = arango_doc["validations"]
        )

    @staticmethod
    def __PromptTemplate_to_arango_doc(prompt : PromptTemplate) -> dict: 
        return {
            "template": prompt.template,
            "args" : prompt.args,
            "id" : prompt.id.__str__()
        }

    @staticmethod
    def __LLModel_to_arango_doc(model : LLModel) -> dict:
        return {
            "_key": model.name,
            "main_prompt": ArangoModelStorage.__PromptTemplate_to_arango_doc(model.main_prompt),
            "prompt_alternatives": [ ArangoModelStorage.__PromptTemplate_to_arango_doc(p) 
                                     for p in model.prompt_alternatives],
            "validations": model.validations
        }

    def get_model(self, name : str ) -> LLModel:
        model = self.collection.get(name)
        if model is not None:
            return self.__arango_doc_to_LLModel(model)
        raise BusinessRuleException(detail=f"{name} is not a registered model")
    
    def delete_model(self, name):
        try:
            self.collection.delete(name)
            return True
        except DocumentDeleteError:
            return False

    def add_model(self, model : LLModel):
        try:
            self.collection.insert(self.__LLModel_to_arango_doc(model))
        except DocumentInsertError:
            raise BusinessRuleException(detail=f"{model.name} is already registered")

    def update_model(self, model : LLModel):
        try:
            self.collection.update(self.__LLModel_to_arango_doc(model))
        except DocumentUpdateError:
            self.collection.insert(self.__LLModel_to_arango_doc(model))
    
    def list_models(self):
        return [model for model in self.db.aql.execute(f"FOR model IN {self.collection_name} RETURN model._key")]
