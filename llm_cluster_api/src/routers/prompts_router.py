from src.decorators.business_rule_exception_check import business_rule_exception_check
from fastapi import APIRouter, HTTPException
from db.model_storage import ModelStorage
from src.models.prompt import Prompt
from uuid import UUID
import uuid

prompts_router = APIRouter()

@prompts_router.get('/models/{name}/prompts', tags=["Prompt" ])
@business_rule_exception_check
def get_prompts(name : str):
    return ModelStorage.get_model(name).list_prompts()

@prompts_router.get('/models/{name}/prompts/{prompt_uid}', tags=["Prompt" ])
@business_rule_exception_check
def get_single_prompt(name : str, prompt_uid : UUID):
    return ModelStorage.get_model(name).get_prompt(prompt_uid)

@prompts_router.post('/models/{name}/prompts', tags=["Prompt"])
@business_rule_exception_check
def post_prompts(name:str, prompts : list[Prompt]):
    new_uids = []
    for prompt in prompts:
        new_uids.append(uuid.uuid4())
        ModelStorage.get_model(name).add_prompt_alternative(
            prompt.to_PromptTemplate(new_uids[-1])
            )
    return new_uids

@prompts_router.put('/models/{name}/prompts}', tags=["Prompt" ])
@business_rule_exception_check
def delete_prompts(name : str, prompt_uids : list[UUID]):
    ModelStorage.get_model(name).remove_prompt_alternatives(prompt_uids)
    return "Ok"

@prompts_router.put('/models/{name}/prompts/main/{prompt_uid}', tags=["Prompt"])
@business_rule_exception_check
def swap_main_prompt(name : str, prompt_uid : UUID):
    ModelStorage.get_model(name).swap_prompt_for_alternative(prompt_uid)
    return "Ok"


@prompts_router.put('/models/{name}/prompts/main', tags=["Prompt"])
@business_rule_exception_check
def swap_main_prompt_to_new(name : str, prompt : Prompt):
    new_uid = uuid.uuid4()
    ModelStorage.get_model(name).main_prompt = prompt.to_PromptTemplate(new_uid)
    return new_uid