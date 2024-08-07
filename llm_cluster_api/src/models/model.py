from src.llm.query_validator import QueryValidator
from src.models.prompt import Prompt
from src.llm.LLModel import LLModel
from fastapi import HTTPException
from pydantic import BaseModel
from uuid import uuid4

class Model(BaseModel):
    model_name : str
    default_prompt : Prompt
    prompt_alternatives : list[Prompt] = []
    validations : list[int] = []

    def to_LLModel(self) -> LLModel:

        for validation in self.validations:
            if not QueryValidator.is_valid_validation(validation):
                raise HTTPException(
                    status_code=400, 
                    detail=f"there is no validation with index {validation}"
                )
        

        return LLModel(
            model_name= self.model_name,
            default_prompt= self.default_prompt.to_PromptTemplate(uuid4()),
            validations= self.validations,
            prompt_alternatives= [ prompt.to_PromptTemplate(uuid4()) for prompt in self.prompt_alternatives]
        )