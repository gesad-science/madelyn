from fastapi import APIRouter, HTTPException
from src.model_storage import ModelStorage
from src.models.prompt import Prompt
from src.llm.prompt_template import PromptTemplate
from uuid import UUID
import uuid

prompts_router = APIRouter()

@prompts_router.get('/models/{model_name}/prompts')
def get_prompts(model_name : str):
    return ModelStorage.get_model(model_name).list_prompts()

@prompts_router.get('/models/{model_name}/prompts/{prompt_uid}')
def get_single_prompt(model_name : str, prompt_uid : UUID):
    return ModelStorage.get_model(model_name).get_prompt(prompt_uid)

@prompts_router.post('/models/{model_name}/prompts')
def post_prompt(model_name:str, prompt : Prompt):
    new_uid = uuid.uuid4()
    ModelStorage.get_model(model_name).add_prompt_alternative(
        PromptTemplate(
                args=prompt.agrs,
                template= prompt.template,
                id=new_uid,
            )
        )
    return new_uid

@prompts_router.delete('/models/{model_name}/prompts/{prompt_uid}')
def delete_single_prompt(model_name : str, prompt_uid : UUID):
    model = ModelStorage.get_model(model_name) 
    if model.main_prompt.id == prompt_uid:
        raise HTTPException(status_code= 400, 
                            detail="Can't delete main prompt from a model. Look for prompt swap to change the main prompt")
    model.remove_prompt_alternative(prompt_uid)
    return "Ok"

@prompts_router.put('/models/{model_name}/prompts/{prompt_uid}')
def swap_main_prompt(model_name : str, prompt_uid : UUID):
    model = ModelStorage.get_model(model_name)
    if model.main_prompt.id == prompt_uid:
        raise HTTPException(status_code=400, detail="You are trying to swap the main prompt by itself")
    prompt = model.get_prompt(prompt_uid)
    main_prompt = model.main_prompt
    model.main_prompt = prompt
    model.add_prompt_alternative(main_prompt)
    return "Ok"


@prompts_router.put('/models/{model_name}/prompts')
def swap_main_prompt_to_new(model_name : str, prompt : Prompt):
    new_uid = uuid.uuid4()
    ModelStorage.get_model(model_name).main_prompt = PromptTemplate(
                                                                    args=prompt.agrs,
                                                                    template= prompt.template,
                                                                    id=new_uid,
                                                                   )
    return new_uid