from uuid import UUID
from fastapi import APIRouter

validations_router = APIRouter()

@validations_router.get('/validations')
def get_validations():
    pass

@validations_router.get('/models/{model_name}/validations')
def get_validations_from_model(model_name : str):
    pass

@validations_router.delete('/models/{model_name}/validations/{validation_number}')
def delete_validations(model_name : str, validation_nuimber : int):
    pass


@validations_router.post('/models/{model_name}/validations/{validation_number}')
def post_validations(model_name : str, validation_nuimber : int):
    pass