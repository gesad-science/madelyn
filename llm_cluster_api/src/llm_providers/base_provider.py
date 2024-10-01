from abc import ABC, abstractmethod
from src.llm.llm_capabilities import LLMCapabilities

class BaseProvider(ABC):
    @abstractmethod
    def list_models(self) -> dict:
        raise NotImplementedError()
    @abstractmethod
    def has_model(self, model : str) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def get_capabilities_of(self, model : str) -> list[LLMCapabilities] | None:
        raise NotImplementedError()

    @abstractmethod
    def make_question_awnser_call(self, prompt : str, model : str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def make_token_classification_call(self, prompt : str, model : str) -> dict:
        raise NotImplementedError()
    
    @abstractmethod
    def make_sentiment_analysis_call(self, prompt : str, model : str) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def make_text_similarity_call(self, text_1 : str, text_2 : str, model : str) -> bool:
        raise NotImplementedError()
    # TOKEN_CLASSIFICATION = 1
    # SENTIMENT_ANALYSIS = 2
    # TEXT_SIMILARITY = 3 
    # question_awnser = 4