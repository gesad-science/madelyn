from src.providers.base_provider import BaseProvider
from src.providers.ollama_provider import OllamaProvider
from src.providers.bedrock_provider import BedrockProvider
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
    def set_default_provider(cls, default):
        cls.__default = default
    
    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        return cls.__providers[cls.__default]

