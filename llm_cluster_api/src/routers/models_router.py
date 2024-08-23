from src.LLM_provider_storage import LLMProviderStorage
from fastapi import APIRouter, HTTPException
from src.db.arango_model_storage import ArangoModelStorage
from src.llm.LLModel import LLModel
from uuid import UUID

from src.models.model import Model
from src.models.query import Query

from src.decorators.business_rule_exception_check import business_rule_exception_check

models_router = APIRouter()

@models_router.get('/models', tags=["Model" ])
@business_rule_exception_check
def get_models():
        return ArangoModelStorage().list_models()

@models_router.get('/models/unregistered', tags=["Model" ])
@business_rule_exception_check
def get_unregistered_models():
    all_models = LLMProviderStorage.get_default_provider().list_models()
    print("passed")
    for model in ArangoModelStorage().list_models():
        if model in all_models:
            all_models.remove(model)
    return all_models

@models_router.get('/models/{name}', tags=["Model" ])
@business_rule_exception_check
def get_model(name : str):
    return ArangoModelStorage().get_model(name).description()


@models_router.delete('/models/{name}', tags=["Model" ])
@business_rule_exception_check
def delete_model(name : str):
    if not ArangoModelStorage().delete_model(name):
        raise HTTPException(status_code=404, detail=f"{name} is not a registered model")
    return "Ok"

@models_router.post('/models', tags=["Model" ])
@business_rule_exception_check
def post_model(model : Model):
    if LLMProviderStorage.get_default_provider().has_model(model.name):
        ArangoModelStorage().add_model(model.to_LLModel())
        return "Ok"

    raise HTTPException(status_code=400, detail=f"There is no support for the {model.name}")

@models_router.put('/models', tags=["Model"])
@business_rule_exception_check
def put_model(model : Model):
    ArangoModelStorage().update_model(model.to_LLModel())
    return "Ok"

@models_router.post('/models/{name}/query', tags=["Query"])
@business_rule_exception_check
def query(name : str, prompt_input : Query):
        return ArangoModelStorage().get_model(name).run_query(
            inputs={
                "variables": prompt_input.variables or []
            }
        )