from src.LLM_provider_storage import LLMProviderStorage

class TextSimilarityService:

    @classmethod
    def make_call(cls, text_1, text_2,  model) -> float:
        return LLMProviderStorage.get_provider_with_model(model).make_text_similarity_call(text_1, text_2, model)