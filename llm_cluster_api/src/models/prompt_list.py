from src.models.prompt import Prompt
from src.llm.prompt_line import PromptLine
from uuid import uuid4
from pydantic import BaseModel

class PromptList(BaseModel):
    default_prompt : Prompt
    prompt_alternatives : list[Prompt] = []

    def to_PromptLine(self):
        return PromptLine(self.default_prompt.to_PromptTemplate(uuid4()), 
                            [ x.to_PromptTemplate(uuid4()) for x in self.prompt_alternatives ]
                          )