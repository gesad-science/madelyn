from abc import ABC
from src.LLM_provider_storage import LLMProviderStorage
from src.utils.tokens_processing import TokensFixer

class TokenClassificationService(ABC):

    @classmethod
    def make_call(cls, model, text) -> list[dict]:
        return TokensFixer.fix_tokens(tokens_list=LLMProviderStorage.get_default_provider().make_token_classification_call(text, model))