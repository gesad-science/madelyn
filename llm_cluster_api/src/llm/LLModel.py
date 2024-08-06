from src.llm.prompt_template import PromptTemplate
from src.LLM_provider_storage import LLMProviderStorage
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

    def get_prompt(self, prompt_template_uid : UUID = None) -> PromptTemplate:
        if prompt_template_uid == None or prompt_template_uid == self.main_prompt.id: 
            return self.main_prompt
        for prompt in self.prompt_alternatives:
            if prompt.id == prompt_template_uid:
                return prompt
        raise HTTPException(
            status_code=400,
            detail= f'cant find prompt alternative f{prompt_template_uid} in {self.model_name}\'s configuration'
            )

    def add_prompt_alternative(self, prompt_template : PromptTemplate):
        self.prompt_alternatives.append(prompt_template)

    def remove_prompt_alternative(self, prompt_template_uid):
        for index, prompt in enumerate(self.prompt_alternatives):
            if prompt.id == prompt_template_uid:
                self.prompt_alternatives.pop(index)
                return True
            
        return False
 
    def run_query(self, inputs : dict, prompt_template_uid : UUID = None):
        prompt = self.get_prompt(prompt_template_uid)

        logs = QueryValidator.validate(prompt, inputs, self.validations)

        if len(logs) != 0:
            return {'logs' : logs }

        return {
            "response" : LLMProviderStorage.get_default_provider().make_call(prompt= prompt.apply_input(inputs),
                                                                             model=self.model_name)
        }

    def add_validation(self, validation_id : int):
        if validation_id not in self.validations:
            self.validations.append(validation_id)
            return True
        return False
        
    def remove_validation(self, validation_id : int):
        if validation_id in self.validations:
            self.validations.remove(validation_id) 
            return True
        return False
    
    def description(self):
        return {
            "name" : self.model_name,
            "main_prompt_uid": self.main_prompt.id,
            "prompt_alternatives_uid" : [ prompt.id for prompt in self.prompt_alternatives],
            "validations" : self.validations
        }    
    
    def list_prompts(self):
        return {
            "main_prompt_uid": self.main_prompt.id,
            "prompt_alternatives_uid" : [ prompt.id for prompt in self.prompt_alternatives],
        }

