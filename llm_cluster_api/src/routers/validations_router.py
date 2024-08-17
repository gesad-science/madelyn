from src.decorators.bad_value_check import bad_value_check
from src.llm.query_validator import QueryValidator
from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from uuid import UUID


validations_router = APIRouter()

@validations_router.get('/validations', tags=["Validation"])
@bad_value_check
def get_validations():
    return QueryValidator.list_all_validations()

@validations_router.get('/models/{name}/validations', tags=["Validation"])
@bad_value_check
def get_validations_from_model(name : str):
    return QueryValidator.list_validations(ModelStorage.get_model(name).validations)

@validations_router.put('/models/{name}/validations',tags=["Validation" ])
@bad_value_check
def delete_validations(name : str, validations : list[int]):
    ModelStorage.get_model(name).remove_validations(validations)

@validations_router.post('/models/{name}/validations', tags=["Validation"])
@bad_value_check
def post_validations(name : str, validations : list[int]):
    ModelStorage.get_model(name).add_validations(validations)
