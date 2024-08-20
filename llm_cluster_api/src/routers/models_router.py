from src.LLM_provider_storage import LLMProviderStorage
from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from src.llm.LLModel import LLModel
from uuid import UUID
from exceptions.business_rule_exception import BusinessRuleException

from src.models.model import Model
from src.models.query import Query

from src.decorators.business_rule_exception_check import business_rule_exception_check

models_router = APIRouter()

@models_router.get('/models', tags=["Model" ])
@business_rule_exception_check
def get_models():
        return ModelStorage.list_models()

@models_router.get('/models/unregistered', tags=["Model" ])
@business_rule_exception_check
def get_unregistered_models():
    all_models = LLMProviderStorage.get_default_provider().list_models()
    for model in ModelStorage.list_models():
        if model in all_models:
            all_models.remove(model)
    return all_models

@models_router.get('/models/{name}', tags=["Model" ])
@business_rule_exception_check
def get_model(name : str):
    return ModelStorage.get_model(name).description()


@models_router.delete('/models/{name}', tags=["Model" ])
@business_rule_exception_check
def delete_model(name : str):
    if not ModelStorage.delete_model(name):
        raise HTTPException(status_code=404, detail=f"{name} is not a registered model")
    return "Ok"

@models_router.post('/models', tags=["Model" ])
@business_rule_exception_check
def post_model(model : Model):
    ModelStorage.add_model(model.to_LLModel())
    return "Ok"

@models_router.put('/models', tags=["Model"])
@business_rule_exception_check
def put_model(model : Model):
    ModelStorage.delete_model(model.name)
    ModelStorage.add_model(model.to_LLModel())
    return "Ok"

@models_router.post('/models/{name}/query', tags=["Query"])
@business_rule_exception_check
def query(name : str, prompt_input : Query):
        return ModelStorage.get_model(name).run_query(
            inputs={
                "variables": prompt_input.variables or []
            }
        )