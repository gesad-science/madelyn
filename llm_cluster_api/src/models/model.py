from src.llm.query_validator import QueryValidator
from src.models.prompt import Prompt
from src.llm.LLModel import LLModel
from exceptions.business_rule_exception import BusinessRuleException
from pydantic import BaseModel
from uuid import uuid4

class Model(BaseModel):
    name : str
    default_prompt : Prompt
    prompt_alternatives : list[Prompt] = []
    validations : list[int] = []

    def to_LLModel(self) -> LLModel:
        illegal_validations = []
        for validation in self.validations:
            if not QueryValidator.is_valid(validation):
                illegal_validations.append(validation)
        if len(illegal_validations) > 0:
            raise BusinessRuleException(detail=f"These are not valid validation numbers {illegal_validations}")

        return LLModel(
            name= self.name,
            default_prompt= self.default_prompt.to_PromptTemplate(uuid4()),
            validations= self.validations,
            prompt_alternatives= [ prompt.to_PromptTemplate(uuid4()) for prompt in self.prompt_alternatives]
        )