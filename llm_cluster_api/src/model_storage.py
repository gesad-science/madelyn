from src.llm.LLModel import LLModel
from abc import ABC
from src.exceptions.bad_value_exception import BadValueException

class ModelStorage(ABC):
    __models : list[LLModel] = []

    # @staticmethod
    @classmethod
    def get_model(cls, name : str ) -> LLModel:
        for model in cls.__models:
            if model.name == name:
                return model
        raise BadValueException(detail=f"{name} is not a registered model")
        
    
    @classmethod
    def delete_model(cls, name):
        for index , model in enumerate(cls.__models):
            if model.name == name:
                cls.__models.pop(index)
                return True
            
        return False

    @classmethod
    def add_model(cls, model : LLModel):
        for m in cls.__models:
            if m.name == model.name:
                raise BadValueException(detail=f"{model.name} is already registered")
        cls.__models.append(model)
    
    @classmethod
    def list_models(cls):
        return [model.name for model in cls.__models]            

    
