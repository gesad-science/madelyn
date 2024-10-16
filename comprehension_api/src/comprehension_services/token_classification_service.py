from abc import ABC
from src.LLM_provider_storage import LLMProviderStorage

class TokenClassificationService(ABC):

    @classmethod
    def make_call(cls, model, text) -> list[dict]:
        return LLMProviderStorage.get_default_provider().make_token_classification_call(text, model)