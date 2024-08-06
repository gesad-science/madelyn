from src.llm.LLModel import LLModel
from fastapi import HTTPException
from abc import ABC

class ModelStorage(ABC):
    __models : list[LLModel] = []

    # @staticmethod
    @classmethod
    def get_model(cls, model_name : str ) -> LLModel:
        for model in cls.__models:
            if model.model_name == model_name:
                return model
        raise HTTPException(
            status_code=400,
            detail=f"{model_name} is not a registered model"
        )
        
    
    @classmethod
    def delete_model(cls, model_name):
        for index , model in enumerate(cls.__models):
            if model.model_name == model_name:
                cls.__models.pop(index)
                return True
            
        return False

    @classmethod
    def add_model(cls, model : LLModel):
        for m in cls.__models:
            if m.model_name == model.model_name:
                raise HTTPException(status_code=400, detail=f"{model.model_name} is already registered")
        cls.__models.append(model)
    
    @classmethod
    def list_models(cls):
        return [model.model_name for model in cls.__models]            

    
