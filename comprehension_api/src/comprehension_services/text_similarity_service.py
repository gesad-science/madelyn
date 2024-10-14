from abc import ABC
from src.LLM_provider_storage import LLMProviderStorage

class TextSimilarityService(ABC):

    @classmethod
    def make_call(cls, text_1, text_2,  model) -> float:
        return LLMProviderStorage.get_default_provider().make_text_similarity_call(text_1, text_2, model)