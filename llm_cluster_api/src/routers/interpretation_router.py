
from fastapi import APIRouter, HTTPException

from src.interpretation_functions.interpretation_functions import Interpretation_module

interpretation_router = APIRouter()

@interpretation_router.get('/interpret/{user_msg}/{model_name}')
def interpret_msg(user_msg : str, model_name : str):
    im = Interpretation_module(user_msg=user_msg, model_name=model_name)
    return Interpretation_module.extract_data()
    
