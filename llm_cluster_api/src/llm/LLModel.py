from src.llm.prompt_template import PromptTemplate
from src.LLM_provider_storage import LLMProviderStorage
from src.exceptions.business_rule_exception import BusinessRuleException

from uuid import UUID
from src.llm.query_validator import QueryValidator

class LLModel():
    def __init__(self,
                 name : str,
                 default_prompt : PromptTemplate, 
                 prompt_alternatives : list[PromptTemplate] = [], 
                 validations : list[int] = []) -> None:
        
        self.main_prompt = default_prompt
        self.prompt_alternatives = prompt_alternatives
        self.validations = validations
        self.name = name
    
    def description(self):
        return {
            "name" : self.name,
            "main_prompt_uid": self.main_prompt.id,
            "prompt_alternatives_uid" : [ prompt.id for prompt in self.prompt_alternatives],
            "validations" : self.validations
        }    
    
    def get_prompt(self, prompt_template_uid : UUID = None) -> PromptTemplate:
        if prompt_template_uid == None or prompt_template_uid == self.main_prompt.id: 
            return self.main_prompt
        for prompt in self.prompt_alternatives:
            if prompt.id == prompt_template_uid:
                return prompt
        raise BusinessRuleException(detail= f'cant find prompt alternative f{prompt_template_uid} in {self.name}\'s configuration')

    def add_prompt_alternative(self, prompt_template : PromptTemplate):
        self.prompt_alternatives.append(prompt_template)

    def remove_prompt_alternatives(self, prompt_template_uids : list[UUID]):
        if self.main_prompt in prompt_template_uids:
            raise BusinessRuleException(
                detail="You cant delete the main prompt."
            )

        for prompt_template_uid in prompt_template_uids:        
            for index, prompt in enumerate(self.prompt_alternatives):
                if prompt.id == prompt_template_uid:
                    self.prompt_alternatives.pop(index)
                    break

    def remove_prompt_alternative(self, prompt_template_uid):
        for index, prompt in enumerate(self.prompt_alternatives):
            if prompt.id == prompt_template_uid:
                self.prompt_alternatives.pop(index)
                return True
            
        return False

    def list_prompts(self):
        return {
            "main_prompt_uid": self.main_prompt.id,
            "prompt_alternatives_uid" : [ prompt.id for prompt in self.prompt_alternatives],
        }

    def swap_prompt_for_alternative(self, prompt_uid):
        if self.main_prompt.id == prompt_uid:
            raise BusinessRuleException(detail="You are trying to swap the main prompt by itself")
        prompt = self.get_prompt(prompt_uid)

        self.remove_prompt_alternative(prompt.id)

        main_prompt = self.main_prompt
        self.main_prompt = prompt
        self.add_prompt_alternative(main_prompt)
        
    def add_validations(self, validations : list[int]) -> tuple[bool, list[int]]:
        invalid_ones = QueryValidator.invalid_validations_from(validations)
        if len(invalid_ones) > 0:
            raise BusinessRuleException(
                detail=f'These are not valid validation numbers: {invalid_ones}'
            )

        for validation in validations:
            self.validations.append(validation)

    def add_validation(self, validation_id : int):
        if validation_id not in self.validations:
            self.validations.append(validation_id)
            return True
        return False
    
    def remove_validations(self, validations : list[int]):
        invalid_ones = QueryValidator.invalid_validations_from(validations)
        if len(invalid_ones) > 0:
            raise BusinessRuleException(
                detail=f'These are not valid validation numbers: {invalid_ones}'
            )

        for validation in validations:
            if validation in self.validations:
                self.validations.remove(validation)

    def remove_validation(self, validation_id : int):
        if validation_id in self.validations:
            self.validations.remove(validation_id) 
            return True
        return False

    def run_question_awnser_query(self, inputs : dict, prompt_template_uid : UUID = None):
        prompt = self.get_prompt(prompt_template_uid)

        logs = QueryValidator.validate(prompt, inputs, self.validations)

        if len(logs) != 0:
            return {'logs' : logs }

        return {
            "response" : LLMProviderStorage.get_provider_with_model(self.name).make_question_awnser_call(prompt= prompt.apply_input(inputs),
                                                                             model=self.name)
        }
    