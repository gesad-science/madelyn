from src.llm.LLModel import LLModel, PromptType
from src.llm.query_validator import QueryValidator
from src.LLM_provider_storage import LLMProviderStorage
from uuid import UUID

class QAService:
    def make_call(self, inputs : dict, prompt_type : PromptType, model : LLModel):

        prompts = model.get_prompts_of_type(prompt_type)

        for prompt in prompts:
            logs = QueryValidator.validate(prompt, inputs, model.validations)

            if len(logs) != 0:
                return {'error' : logs }

            return {
                "response" : LLMProviderStorage.get_default_provider().make_call(prompt= prompt.apply_input(inputs),
                                                                                    model=model.name)
            }
