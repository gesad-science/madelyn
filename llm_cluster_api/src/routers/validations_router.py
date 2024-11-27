from src.decorators.exception_check import exception_check
from src.llm.query_validator import QueryValidator
from fastapi import APIRouter, HTTPException
from src.db.couch_model_storage import CouchModelStorage 
from uuid import UUID


validations_router = APIRouter()

@validations_router.get('/validations', tags=["Validation"])
@exception_check
def get_validations():
    return QueryValidator.list_all_validations()

@validations_router.post('/models/validations/get', tags=["Validation"])
@exception_check
def get_validations_from_model(name : str):
    return QueryValidator.list_validations(CouchModelStorage().get_model(name).validations)

@validations_router.put('/models/validations',tags=["Validation" ])
@exception_check
def delete_validations(name : str, validations : list[int]):
    model_storage = CouchModelStorage()
    model = model_storage.get_model(name)
    model.remove_validations(validations)
    model_storage.update_model(model)
    return "Ok"

@validations_router.post('/models/validations/', tags=["Validation"])
@exception_check
def post_validations(name : str, validations : list[int]):
    model_storage = CouchModelStorage()
    model = model_storage.get_model(name)
    model.add_validations(validations)
    model_storage.update_model(model)
    return "Ok"
