from src.llm.query_validator import QueryValidator
from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from uuid import UUID


validations_router = APIRouter()

@validations_router.get('/validations')
def get_validations():
    return QueryValidator.list_all_validations()

@validations_router.get('/models/{model_name}/validations')
def get_validations_from_model(model_name : str):
    return QueryValidator.list_validations(ModelStorage.get_model(model_name).validations)

@validations_router.delete('/models/{model_name}/validations/{validation_number}')
def delete_validations(model_name : str, validation_number : int):
    if ModelStorage.get_model(model_name).remove_validation(validation_number):
        return "Ok"
    raise HTTPException(status_code=400, detail=f"Couldn't find validation {validation_number} in model {model_name}")

@validations_router.post('/models/{model_name}/validations/{validation_number}')
def post_validations(model_name : str, validation_number : int):
    if ModelStorage.get_model(model_name).add_validation(validation_number):
        return 'Ok'
    raise HTTPException(status_code=400, detail=f"Validation {validation_number} already registered in model {model_name}")
    