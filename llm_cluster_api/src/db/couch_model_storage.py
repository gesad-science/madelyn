from src.exceptions.business_rule_exception import BusinessRuleException
from src.llm.prompt_template import PromptTemplate
from src.llm.prompt_line import PromptLine
# from src.LLM_provider_storage import LLMProviderStorage
# from src.utils.singleton import Singleton
from src.llm.LLModel import LLModel
from uuid import UUID
from couchdb import Server
from couchdb.http import ResourceConflict, ResourceNotFound

# from src.consts import ARANGODB_COLLECTION_NAME, ARANGODB_DATABASE_NAME, ARANGODB_PASSWORD, ARANGODB_URL, ARANGODB_USERNAME
"""
Acourding to a fast research pyarango is not thread safe by default, so
initially im just going to init a new connection for each db interaction
"""
class CouchModelStorage:

    def __init__(self, url = "http://localhost:5984", user = "admin", password = "123", db_name = "madelyn_model_db") -> None:
        self.server = Server(url)
        self.server.resource.credentials = (user, password)
        self.db_name = db_name

        if not (self.db_name in self.server):     
            self.server.create(self.db_name)
        self.db = self.server[self.db_name]
        
    def get_rev_of(self, id : str) -> str:
        mango = {
                    "selector" : {'_id': id},
                    "fields" : ["_rev"]
                }

        res = [dict(x).get("_rev", None) for x in list(self.db.find(mango))]

        return res[0] if len(res) == 1 else None

    @staticmethod
    def __couch_doc_to_PromptTemplate(arango_doc : dict) -> PromptTemplate: 
        return PromptTemplate(
            template= arango_doc["template"],
            args= arango_doc["args"],
            id= UUID(arango_doc["id"])
        )

    @staticmethod
    def __couch_doc_to_PromptLine(couch_doc : dict) -> PromptLine:
        return PromptLine(
            main_prompt=CouchModelStorage.__couch_doc_to_PromptTemplate(couch_doc["main_prompt"]),
            prompt_alternatives=[
                CouchModelStorage.__couch_doc_to_PromptTemplate(x) for x in couch_doc["prompt_alternatives"]
            ]
        )

    @staticmethod
    def __couch_doc_to_LLModel(couch_doc : dict) -> LLModel:
        return LLModel(
            name = couch_doc["_id"],
            intent= CouchModelStorage.__couch_doc_to_PromptLine(couch_doc["intent"]),
            entity= CouchModelStorage.__couch_doc_to_PromptLine(couch_doc["entity"]),
            filter= CouchModelStorage.__couch_doc_to_PromptLine(couch_doc["filter"]),
            attribute= CouchModelStorage.__couch_doc_to_PromptLine(couch_doc["attribute"]),
            validations = couch_doc["validations"]
        )

    @staticmethod
    def __PromptTemplate_to_couch_doc(prompt : PromptTemplate) -> dict: 
        return {
            "template": prompt.template,
            "args" : prompt.args,
            "id" : prompt.id.__str__()
        }

    @staticmethod
    def __PromptLine_to_couch_doc(prompt_line : PromptLine) -> dict: 
        return {
            "main_prompt": CouchModelStorage.__PromptTemplate_to_couch_doc(prompt_line.main_prompt),
            "prompt_alternatives": [
                CouchModelStorage.__PromptTemplate_to_couch_doc(x) for x in prompt_line.prompt_alternatives
            ]
        }

    @staticmethod
    def __LLModel_to_couch_doc(model : LLModel, rev = None) -> dict:
        ans = {
            "_id": model.name,
            "filter":  CouchModelStorage.__PromptLine_to_couch_doc(model.filter),
            "entity":  CouchModelStorage.__PromptLine_to_couch_doc(model.entity),
            "intent":  CouchModelStorage.__PromptLine_to_couch_doc(model.intent),
            "attribute":  CouchModelStorage.__PromptLine_to_couch_doc(model.attribute),
            "validations": model.validations
        }

        if rev is not None:
            ans["_rev"] = rev

        return ans

    def get_model(self, name : str ) -> LLModel:
        model = self.db.get(name)
        if model is not None:
            return self.__couch_doc_to_LLModel(model)
        raise BusinessRuleException(detail=f"{name} is not a registered model")
    
    def delete_model(self, name):
        try:
            self.db.delete({"_id":name, "_rev": self.get_rev_of(name)})
            return True
        except ResourceNotFound:
            return False

    def add_model(self, model : LLModel):
        try:
            self.db.save(self.__LLModel_to_couch_doc(model))
        except ResourceConflict:
            raise BusinessRuleException(detail=f"{model.name} is already registered")

    def update_model(self, model : LLModel):
        #TODO

        rev = self.get_rev_of(model.name)
        self.db.save(self.__LLModel_to_couch_doc(model, rev))
    
    def list_models(self):
        mango = {
                "selector" : {},
                "fields" : ["_id"]
            }

        return [{"name" : x["_id"] }for x in list(self.db.find(mango))]
