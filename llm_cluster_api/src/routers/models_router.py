from src.LLM_provider_storage import LLMProviderStorage
from fastapi import APIRouter, HTTPException
from src.db.arango_qa_model_storage import ArangoQAModelStorage
from src.llm.comprehension_services.question_awnser_service import QuestionAwnserService
from src.llm.LLModelQA import LLModelQA
from uuid import UUID

from src.models.model import Model

from src.decorators.business_rule_exception_check import business_rule_exception_check

models_router = APIRouter()

@models_router.get('/models', tags=["Model" ])
@business_rule_exception_check
def get_models():
        return ArangoQAModelStorage().list_models()

@models_router.get('/models/unregistered', tags=["Model" ])
@business_rule_exception_check
def get_unregistered_models():

    # HORRIVEL

    models = LLMProviderStorage.list_all_models() 
    model_names = [ model['name'] for model in models]

    registered_names = [model["name"] for model in ArangoQAModelStorage().list_models()]
    to_remove = []

    for i, model in enumerate(model_names):
        if model in registered_names:
             to_remove.append(i)
    for i in to_remove[::-1]:
        models.pop(i)


    return models

@models_router.post('/models/get', tags=["Model"])
@business_rule_exception_check
def get_model(name : str):
    return ArangoQAModelStorage().get_model(name).description()


@models_router.post('/models/delete', tags=["Model" ])
@business_rule_exception_check
def delete_model(name : str):
    if not ArangoQAModelStorage().delete_model(name):
        raise HTTPException(status_code=404, detail=f"{name} is not a registered model")
    return "Ok"

@models_router.post('/models', tags=["Model" ])
@business_rule_exception_check
def post_model(model : Model):
    if LLMProviderStorage.has_model(model.name):
        ArangoQAModelStorage().add_model(model.to_LLModelQA())
        return "Ok"

    raise HTTPException(status_code=400, detail=f"There is no support for the {model.name}")

@models_router.put('/models', tags=["Model"])
@business_rule_exception_check
def put_model(model : Model):
    if not LLMProviderStorage.has_model(model=model.name):
         raise HTTPException(detail=f"Cant find {model.name} in any providers", status_code=400)
    ArangoQAModelStorage().update_model(model.to_LLModelQA())
    return "Ok"
