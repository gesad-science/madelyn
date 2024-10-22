from src.llm.prompt_template import PromptTemplate
from dataclasses import dataclass

@dataclass
class PromptLine:
    main_prompt : PromptTemplate
    prompt_alternatives : list[PromptTemplate]

    def list_prompts(self):
        return {
            "main_prompt_uid": self.main_prompt.id,
            "prompt_alternatives_uid" : [ prompt.id for prompt in self.prompt_alternatives],
        }
    
    def __iter__(self):
        yield self.main_prompt

        for prompt in self.prompt_alternatives:
            yield prompt

