from src.decorators.bad_value_check import bad_value_check
from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from src.models.prompt import Prompt
from uuid import UUID
import uuid

prompts_router = APIRouter()

@prompts_router.get('/models/{name}/prompts', tags=["Prompt" ])
@bad_value_check
def get_prompts(name : str):
    return ModelStorage.get_model(name).list_prompts()

@prompts_router.get('/models/{name}/prompts/{prompt_uid}', tags=["Prompt" ])
@bad_value_check
def get_single_prompt(name : str, prompt_uid : UUID):
    return ModelStorage.get_model(name).get_prompt(prompt_uid)

@prompts_router.post('/models/{name}/prompts', tags=["Prompt"])
@bad_value_check
def post_prompts(name:str, prompts : list[Prompt]):
    new_uids = []
    for prompt in prompts:
        new_uids.append(uuid.uuid4())
        ModelStorage.get_model(name).add_prompt_alternative(
            prompt.to_PromptTemplate(new_uids[-1])
            )
    return new_uids

@prompts_router.put('/models/{name}/prompts}', tags=["Prompt" ])
@bad_value_check
def delete_prompts(name : str, prompt_uids : list[UUID]):
    ModelStorage.get_model(name).remove_prompt_alternatives(prompt_uids)
    return "Ok"

@prompts_router.put('/models/{name}/prompts/main/{prompt_uid}', tags=["Prompt"])
@bad_value_check
def swap_main_prompt(name : str, prompt_uid : UUID):
    model = ModelStorage.get_model(name)
    if model.main_prompt.id == prompt_uid:
        raise HTTPException(status_code=400, detail="You are trying to swap the main prompt by itself")
    prompt = model.get_prompt(prompt_uid)

    model.remove_prompt_alternative(prompt.id)

    main_prompt = model.main_prompt
    model.main_prompt = prompt
    model.add_prompt_alternative(main_prompt)
    return "Ok"


@prompts_router.put('/models/{name}/prompts/main', tags=["Prompt"])
@bad_value_check
def swap_main_prompt_to_new(name : str, prompt : Prompt):
    new_uid = uuid.uuid4()
    ModelStorage.get_model(name).main_prompt = prompt.to_PromptTemplate(new_uid)
    return new_uid