from uuid import UUID
from fastapi import APIRouter

models_router = APIRouter()

@models_router.get('/models/{model_name}')
def get_models(model_name : str):
    pass

@models_router.get('/models')
def get_models():
    pass

@models_router.get('/models/unregistered')
def get_unregistered_models():
    pass

@models_router.post('/models')
def get_unregistered_models(model : Model):
    pass

@models_router.delete('/models/{model_name}')
def get_unregistered_models(model_name : str):
    pass

@models_router.post('/models/{model_name}/query')
def get_unregistered_models(model_name : str, prompt_input : PromptInput):
    pass