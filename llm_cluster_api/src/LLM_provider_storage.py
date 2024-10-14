from src.llm_providers.base_provider import BaseProvider
from src.llm_providers.ollama_provider import OllamaProvider
from abc import ABC
import os
from src.consts import OLLAMA_BASE_URL

class LLMProviderStorage(ABC):
    __providers : dict[str, BaseProvider] = {
        # 'bedrock' : BedrockProvider(),
        'ollama' : OllamaProvider(OLLAMA_BASE_URL)
    }

    __default = 'ollama'

    # @staticmethod
    @classmethod
    def get_provider(cls, provider_name):
        return cls.__providers[provider_name]
    
    @classmethod
    def set_default_provider(cls, default):
        cls.__default = default
    
    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        return cls.get_provider(cls.__default)

