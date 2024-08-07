from src.llm.prompt_template import PromptTemplate
from pydantic import BaseModel
from uuid import UUID

class Prompt(BaseModel):
    template: str
    args : dict

    @classmethod
    def __validate_args(self, args):
        return args

    def to_PromptTemplate(self, id) -> PromptTemplate:
        return PromptTemplate(
            template=self.template,
            args = self.__validate_args(self.args),
            id=id
        )
