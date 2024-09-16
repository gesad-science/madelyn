from src.llm_providers.bedrock_provider import BedrockProvider
from src.llm_providers.ollama_provider import OllamaProvider
from src.llm_providers.base_provider import BaseProvider
from src.exceptions.business_rule_exception import BusinessRuleException
from abc import ABC
import os

class LLMProviderStorage(ABC):
    __providers : dict[str, BaseProvider] = {
        # 'bedrock' : BedrockProvider(),
        'ollama' : OllamaProvider(os.environ.get('OLLAMA_BASE_URL')),
    }

    __default = 'ollama'

    # @staticmethod
    @classmethod
    def get_provider(cls, provider_name):
        return cls.__providers[provider_name]
    
    @classmethod
    def set_default_provider(cls, default : str):
        cls.__default = default
    
    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        return cls.get_provider(cls.__default)
    



    
    @classmethod
    def get_provider_with_model(cls, model : str):
        for provider in cls.__providers.values():
            if provider.has_model(model):
                return provider
        raise BusinessRuleException(f"Cant find {model} in any model provider")
    
    @classmethod
    def list_all_models(cls):
        model_list = set()

        for provider in cls.__providers.values():
            model_list =  model_list | set(provider.list_models())
        return list(model_list)

    @classmethod
    def has_model(cls, model : str):
        for provider in cls.__providers.values():
            if provider.has_model(model):
                return True
        return False