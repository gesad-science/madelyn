from uuid import UUID
from fastapi import APIRouter

prompts_router = APIRouter()

@prompts_router.get('/models/{model_name}/prompts')
def get_prompts(model_name : str):
    pass

@prompts_router.get('/models/{model_name}/prompts/{prompt_uid}')
def get_single_prompt(model_name : str, prompt_uid : UUID):
    pass

@prompts_router.post('/models/{model_name}/prompts')
def post_prompt(model_name:str, Prompt : Prompt):
    pass

@prompts_router.delete('/models/{model_name}/prompts/{prompt_uid}')
def get_single_prompt(model_name : str, prompt_uid : UUID):
    pass

@prompts_router.put('/models/{model_name}/prompts/{prompt_uid}')
def swap_main_prompt(model_name : str, prompt_uid : UUID):
    pass

@prompts_router.put('/models/{model_name}/prompts')
def swap_main_prompt_to_new(model_name : str, prompt : Prompt):
    pass