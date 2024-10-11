from arango import ArangoClient, DocumentDeleteError, DocumentUpdateError, DocumentInsertError
from src.exceptions.business_rule_exception import BusinessRuleException
from src.llm.prompt_template import PromptTemplate
from src.LLM_provider_storage import LLMProviderStorage
# from src.utils.singleton import Singleton
from src.llm.comprehension_services.comprehension_functions import ComprehensionFunctions
from src.llm.LLModelQA import LLModelQA
from uuid import UUID
from couchdb import Server

from src.consts import ARANGODB_COLLECTION_NAME, ARANGODB_DATABASE_NAME, ARANGODB_PASSWORD, ARANGODB_URL, ARANGODB_USERNAME
"""
Acourding to a fast research pyarango is not thread safe by default, so
initially im just going to init a new connection for each db interaction
"""
class CouchQAModelStorage():

    def __init__(self) -> None:
        self.server = Server()
        self.db_name = "tests"

        if self.db_name in self.server:     
            self.server.create(self.db_name)
        self.db = self.server[self.db_name]
        

    def get_rev_of(self, id : str) -> str:
        mango = {
                    "selector" : {'_id': id},
                    "fields" : ["_rev"]
                }

        try:
            return [dict(x)["_rev"] for x in list(self.db.find(mango))][0]
        except Exception:
            return None

    @staticmethod
    def __couch_doc_to_PromptTemplate(arango_doc : dict) -> PromptTemplate: 
        return PromptTemplate(
            template= arango_doc["template"],
            args= arango_doc["args"],
            id= UUID(arango_doc["id"])
        )

    @staticmethod
    def __couch_doc_to_LLModelQA(arango_doc : dict) -> LLModelQA:
        return LLModelQA(
            name = arango_doc["_id"],
            default_prompt=  CouchQAModelStorage.__couch_doc_to_PromptTemplate(arango_doc["main_prompt"]),
            prompt_alternatives=[ CouchQAModelStorage.__couch_doc_to_PromptTemplate(p) 
                                  for p in arango_doc["prompt_alternatives"]],
            validations = arango_doc["validations"]
        )

    @staticmethod
    def __PromptTemplate_to_couch_doc(prompt : PromptTemplate) -> dict: 
        return {
            "template": prompt.template,
            "args" : prompt.args,
            "id" : prompt.id.__str__()
        }

    @staticmethod
    def __LLModelQA_to_couch_doc(model : LLModelQA, rev = None) -> dict:
        ans = {
            "_id": model.name,
            "main_prompt": CouchQAModelStorage.__PromptTemplate_to_couch_doc(model.main_prompt),
            "prompt_alternatives": [ CouchQAModelStorage.__PromptTemplate_to_couch_doc(p) 
                                     for p in model.prompt_alternatives],
            "validations": model.validations
        }

        if rev is not None:
            ans["_rev"] = rev

        return ans

    def get_model(self, name : str ) -> LLModelQA:
        model = self.collection.get(name)
        if model is not None:
            return self.__couch_doc_to_LLModelQA(model)
        raise BusinessRuleException(detail=f"{name} is not a registered model")
    
    def delete_model(self, name):
        try:
            self.db.delete({"_id":name, "_rev": self.get_rev_of(name)})
            return True
        except Exception:
            return False

    def add_model(self, model : LLModelQA):
        cf = LLMProviderStorage.get_provider_with_model(model.name).get_comprehension_functions_of(model.name)
        if  ComprehensionFunctions.QUESTION_AWNSER not in cf if cf else []:
            raise BusinessRuleException(detail=f"Cant register models that are nota capable of QUESTION_AWNSER")

        try:
            self.db.save(self.__LLModelQA_to_couch_doc(model))
        except DocumentInsertError:
            raise BusinessRuleException(detail=f"{model.name} is already registered")

    def update_model(self, model : LLModelQA):
        #TODO

        try:
            rev = self.get_rev_of(model.name)
            self.collection.update(self.__LLModelQA_to_couch_doc(model, rev))

        except DocumentUpdateError:
            self.collection.insert(self.__LLModelQA_to_couch_doc(model))
    
    def list_models(self):
        mango = {
                "selector" : {},
                "fields" : ["_id"]
            }

        return [dict(x) for x in list(self.db.find(mango))]
