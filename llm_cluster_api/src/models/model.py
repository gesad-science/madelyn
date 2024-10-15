from src.llm.query_validator import QueryValidator
from src.models.prompt import Prompt
from src.llm.LLModel import LLModel
from src.exceptions.business_rule_exception import BusinessRuleException
from src.models.prompt_list import PromptList
from pydantic import BaseModel
from uuid import uuid4

class Model(BaseModel):
    name : str
    intent : PromptList
    entity : PromptList
    attribute : PromptList
    filter : PromptList
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
            attribute=self.attribute.to_PromptLine(),
            intent=self.intent.to_PromptLine(),
            entity=self.entity.to_PromptLine(),
            filter=self.filter.to_PromptLine(),
            validations= self.validations,
        )