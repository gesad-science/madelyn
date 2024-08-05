from src.llm.prompt_template import PromptTemplate
from LLMProviderStorage import LLMProviderStorage
from fastapi import HTTPException
from uuid import UUID
from src.llm.query_validator import QueryValidator

class LLModel():
    def __init__(self,
                 model_name : str,
                 default_prompt : PromptTemplate, 
                 prompt_alternatives : list[PromptTemplate] = [], 
                 validations : list[int] = []) -> None:
        
        self.main_prompt = default_prompt
        self.prompt_alternatives = prompt_alternatives
        self.validations = validations
        self.model_name = model_name

    def find_prompt(self, prompt_template_id : UUID = None) -> PromptTemplate:
        if prompt_template_id == None or prompt_template_id == self.main_prompt.id: 
            return self.main_prompt
        for prompt in self.prompt_alternatives:
            if prompt.id == prompt_template_id:
                return prompt
        raise HTTPException(
            status_code=400,
            detail= f'cant find prompt alternative f{prompt_template_id} in {self.model_name}\'s configuration'
            )

    def run_query(self, inputs : dict, prompt_template_id : UUID = None):
        prompt = self.find_prompt(prompt_template_id)

        logs = QueryValidator.validate(prompt, inputs, self.validations)

        if len(logs) != 0:
            return {'logs' : logs }

        return {
            "response" : LLMProviderStorage.get_default_provider().make_call(prompt.apply_input(inputs), self.model_name)
        }

    def add_validation(self, validation_id : int):
        if validation_id not in self.validations:
            self.validations.append(validation_id)
        
    def remove_validation(self, validation_id : int):
        self.validations.remove(validation_id)