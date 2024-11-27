from src.llm_providers.ollama_provider import OllamaProvider
from src.llm_providers.base_provider import BaseProvider
from src.consts import OLLAMA_BASE_URL, HUGGINGFACE_BASE_URL
from abc import ABC
from src.llm_providers.huggingface_provider import HuggingFaceProvider

from src.exceptions.business_rule_exception import BusinessRuleException

import os

class LLMProviderStorage(ABC):
    __providers : dict[str, BaseProvider] = {
        'huggingface' : HuggingFaceProvider(HUGGINGFACE_BASE_URL),
        'ollama' : OllamaProvider(OLLAMA_BASE_URL),
    }

    __default = 'ollama'

    @classmethod
    def get_provider(cls, provider_name):
        return cls.__providers[provider_name]
    
    @classmethod
    def set_default_provider(cls, default):
        cls.__default = default

    @classmethod
    def list_provider(cls):
        return list(cls.__providers.values())
    

    @classmethod
    def get_provider_of(cls, model):
        for provider in cls.__providers.values():
                if provider.has_model(model):
                    return provider
                
        raise BusinessRuleException(detail=f"There is no provider that supports {model}")
    
    

    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        return cls.get_provider(cls.__default)

