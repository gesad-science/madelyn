from src.llm.prompt_template import PromptTemplate
from LLMProviderStorage import LLMProviderStorage
from fastapi import HTTPException
from uuid import UUID

class LLModel():
    def __init__(self,
                 model_name : str,
                 default_prompt : PromptTemplate, 
                 prompt_alternatives : list[PromptTemplate] = [], 
                 validations : list[int, dict] = []) -> None:
        
        self.main_prompt = default_prompt
        self.prompt_alternatives = prompt_alternatives
        self.validations = validations
        self.model_name = model_name

    def run_query(self, query) -> None:
        """
        Run queries to the specified model, based on a 
        defined prompt
        """
        pass

    def __apply_inputs(self, inputs : dict, prompt_template_id : UUID = None) -> str:
        if prompt_template_id == self.main_prompt.id or prompt_template_id == None:
            raise NotImplementedError("Implement a function to fill the template paramethers")
        for prompt in self.prompt_alternatives:
            if prompt_template_id == prompt.id:
                raise NotImplementedError("Implement a function to fill the template paramethers")

        raise HTTPException(
                    status_code=400,
                    detail= f'cant find prompt alternative f{prompt_template_id} in {self.model_name}\'s configuration'
                    )

    def run_query(self, inputs : dict, prompt_template_id : UUID):
        plain_prompt = self.__apply_inputs(inputs, prompt_template_id)

        return LLMProviderStorage.get_default_provider().make_call(plain_prompt, self.model_name)
    