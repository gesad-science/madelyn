from src.LLM_provider_storage import LLMProviderStorage

class SentimentAnalysisService:

    @classmethod
    def make_call(cls, model, text) -> list[dict]:
        return LLMProviderStorage.get_provider_with_model(model).make_sentiment_analysis_call(text, model)