from src.llm.prompt_template import PromptTemplate
from src.LLM_provider_storage import LLMProviderStorage
from src.exceptions.business_rule_exception import BusinessRuleException

from uuid import UUID
from src.llm.query_validator import QueryValidator

from src.llm.prompt_line import  PromptLine
from enum import Enum

class PromptType(Enum):
    INTENT = 'intent' 
    ENTITY = 'entity' 
    ATTRIBUTE = 'attribute'
    FILTER = 'filter' 

class LLModel():
    def __init__(self,
                 name : str,
                 intent : PromptLine,
                 entity : PromptLine,
                 attribute : PromptLine,
                 filter : PromptLine,
                 validations : list[int] = []) -> None:
        
        self.intent = intent
        self.entity = entity
        self.attribute = attribute
        self.filter = filter

        self.__prompt_types = {
            PromptType.INTENT : self.intent,
            PromptType.ENTITY : self.entity,
            PromptType.ATTRIBUTE : self.attribute,
            PromptType.FILTER : self.filter,
        }

        self.validations = validations
        self.name = name

    def get_prompt(self, prompt_template_uid : UUID = None, prompt_type : PromptType = None) -> PromptTemplate:
        if prompt_template_uid is None and prompt_type is None:
            raise BusinessRuleException(detail="prompt_template_uid cant be None at the same time as prompt_type")

        for curr_type, prompt_source in self.__prompt_types.items():
            if prompt_type is not None and prompt_type != curr_type:
                continue

            if prompt_template_uid == None or prompt_template_uid == prompt_source.main_prompt.id: 
                return prompt_source.main_prompt
            for prompt in prompt_source.prompt_alternatives:
                if prompt.id == prompt_template_uid:
                    return prompt
        

        raise BusinessRuleException(detail= f'cant find prompt alternative f{prompt_template_uid} in {self.name}\'s configuration')

    def add_prompt_alternative(self, prompt_template : PromptTemplate, prompt_type : PromptType):
        self.__prompt_types[prompt_type].prompt_alternatives.append(prompt_template)

    def remove_prompt_alternative(self, prompt_template_uid):
        for prompt_source in self.__prompt_types.values():
            for index, prompt in enumerate(prompt_source.prompt_alternatives):
                if prompt.id == prompt_template_uid:
                    prompt_source.prompt_alternatives.pop(index)
                    return True
            
        return False
 
    def remove_prompt_alternatives(self, prompt_template_uids : list[UUID]):
        for prompt_source in self.__prompt_types.values():
            if prompt_source.main_prompt in prompt_template_uids:
                raise BusinessRuleException(
                    detail="You cant delete the main prompt."
                )

        for prompt_template_uid in prompt_template_uids:        
            self.remove_prompt_alternative(prompt_template_uid)

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
    
    def remove_validation(self, validation_id : int):
        if validation_id in self.validations:
            self.validations.remove(validation_id) 
            return True
        return False

    def remove_validations(self, validations : list[int]):
        invalid_ones = QueryValidator.invalid_validations_from(validations)
        if len(invalid_ones) > 0:
            raise BusinessRuleException(
                detail=f'These are not valid validation numbers: {invalid_ones}'
            )

        for validation in validations:
            self.remove_validation(validation)

    def list_prompts(self):
        return dict(
            (p_type, p_source.list_prompts()) for p_type, p_source in self.__prompt_types.items()
        )

    def description(self):
        return {
            "name" : self.name,
            "prompts" : self.list_prompts(),
            "validations" : self.validations
        }    
    
    def swap_prompt_for_alternative(self, prompt_uid, prompt_type : PromptType):
        
        propmt_source = self.__prompt_types[prompt_type]

        if propmt_source.main_prompt.id == prompt_uid:
            raise BusinessRuleException(detail="You are trying to swap the main prompt by itself")
        prompt = self.get_prompt(prompt_uid, prompt_type)

        self.remove_prompt_alternative(prompt.id)

        main_prompt = self.main_prompt
        self.main_prompt = prompt
        self.add_prompt_alternative(main_prompt)
        
    def get_prompts_of_type(self, prompt_type : PromptType) -> PromptLine:
        return self.__prompt_types[prompt_type]