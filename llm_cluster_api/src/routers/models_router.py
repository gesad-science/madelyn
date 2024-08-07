from src.LLM_provider_storage import LLMProviderStorage
from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from src.llm.LLModel import LLModel
from uuid import UUID

from src.models.model import Model
from src.models.query import Query

models_router = APIRouter()

@models_router.get('/models', tags=["Model" ])
def get_models():
    return ModelStorage.list_models()

@models_router.get('/models/unregistered', tags=["Model" ])
def get_unregistered_models():
    all_models = LLMProviderStorage.get_default_provider().list_models()
    for model in ModelStorage.list_models():
        if model in all_models:
            all_models.remove(model)
    return all_models

@models_router.get('/models/{model_name}', tags=["Model" ])
def get_model(model_name : str):
    return ModelStorage.get_model(model_name).description()


@models_router.delete('/models/{model_name}', tags=["Model" ])
def delete_model(model_name : str):
    if not ModelStorage.delete_model(model_name):
        raise HTTPException(status_code=404, detail=f"{model_name} is not a registered model")
    return "Ok"

@models_router.post('/models', tags=["Model" ])
def post_model(model : Model):
    ModelStorage.add_model(model.to_LLModel())
    return "Ok"

@models_router.put('/models', tags=["Model"])
def put_model(model : Model):
    ModelStorage.delete_model(model.name)
    ModelStorage.add_model(model.to_LLModel())
    return "Ok"

@models_router.post('/models/{model_name}/query', tags=["Query"])
def query(model_name : str, prompt_input : Query):
        return ModelStorage.get_model(model_name).run_query(
            inputs={
                "variables": prompt_input.variables or []
            }
        )