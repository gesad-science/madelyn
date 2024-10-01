from src.llm_providers.base_provider import BaseProvider

from src.llm.llm_capabilities import LLMCapabilities
import requests
from src.utils.similarity import cos_sim


from src.exceptions.business_rule_exception import BusinessRuleException

#https://huggingface.co/api/tasks
class HuggingFaceProvider(BaseProvider):

    def __init__(self, base_url, token, required_models : list[dict[str, list[str] | str]]) -> None:
        self.token = token
        self.base_url = base_url
        self.__model_capabilies = dict()
        for model in required_models:
            self.__model_capabilies[model["name"]] = [LLMCapabilities(x) for x in model["capabilities"]]


    def __assemble_base_request(self, prompt, model):
        return { 
                "json" : {"inputs": prompt, "options": {"use_cache": True, "wait_for_model": True}},
                "headers":{"Authorization": f"Bearer {self.token}"}
               }

    def get_capabilities_of(self, model : str) -> list[LLMCapabilities] | None:
        return self.__model_capabilies.get(model, None)

    def list_models(self) -> dict:
        return [ {"name" : x, "capabilities" : self.__model_capabilies[x]} for x in self.__model_capabilies] 
        
    def has_model(self, model : str) -> bool:
        return model in self.__model_capabilies
    
    def make_question_awnser_call(self, prompt : str, model : str) -> str:
        if LLMCapabilities.QUESTION_AWNSER not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do question awnser")
        
        response = requests.post(f"{self.base_url}/models/{model}", **self.__assemble_base_request(prompt, model))
        if not response.ok:
            raise BusinessRuleException(detail=f"From hugging face interface: {response.json()}", private = True, mask_detail="Can't connect to hugging face LLM provider")
        
        return response.json()
    
    def make_token_classification_call(self, prompt : str, model : str) -> dict:
        if LLMCapabilities.TOKEN_CLASSIFICATION not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do token classification")
        
        response = requests.post(f'{self.base_url}/pipeline/token-classification/{model}', **self.__assemble_base_request(prompt, model))
        if not response.ok:
            raise BusinessRuleException(detail=f"From hugging face interface: {response.json()}", private = True, mask_detail="Can't connect to hugging face LLM provider")
        
        return response.json()
    
    def make_sentiment_analysis_call(self, prompt : str, model : str) -> dict:
        if LLMCapabilities.SENTIMENT_ANALYSIS not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do token sentiment analysis")
        
        response = requests.post(f'{self.base_url}/pipeline/token-classification/{model}', **self.__assemble_base_request(prompt, model))
        if not response.ok:
            raise BusinessRuleException(detail=f"From hugging face interface: {response.json()}", private = True, mask_detail="Can't connect to hugging face LLM provider")
        
        return response.json()

    def make_text_similarity_call(self, text_1 : str, text_2 : str, model : str) -> bool:
        if LLMCapabilities.TEXT_SIMILARITY not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do text similarity")
        
        response = requests.post(f'{self.base_url}/pipeline/feature-extraction/{model}', self.__assemble_base_request([text_1, text_2], model))

        if not response.ok:
            raise BusinessRuleException(detail=f"From hugging face interface: {response.json()}", private = True, mask_detail="Can't connect to hugging face LLM provider")
        
        parsed = response.json()

        return cos_sim(parsed[0], parsed[1])