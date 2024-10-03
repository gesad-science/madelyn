from src.LLM_provider_storage import LLMProviderStorage

class TokenClassificationService:

    @classmethod
    def make_call(cls, model, text) -> list[dict]:
        return LLMProviderStorage.get_provider_with_model(model).make_token_classification_call(text, model)