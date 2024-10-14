from src.exceptions.business_rule_exception import BusinessRuleException
from src.providers.hugging_face_provider import HuggingFaceProvider
from src.providers.base_provider import BaseProvider
from abc import ABC


from src.consts import HUGGING_FACE_MODELS, HUGGING_FACE_BASE_URL, HUGGING_FACE_TOKEN

class LLMProviderStorage(ABC):
    __providers : dict[str, BaseProvider] = {
        'hugging_face' : HuggingFaceProvider(base_url= HUGGING_FACE_BASE_URL, required_models=HUGGING_FACE_MODELS),
    }

    __default = 'hugging_face'

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
