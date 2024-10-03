from abc import ABC, abstractmethod
from src.llm.comprehension_services.comprehension_functions import ComprehensionFunctions

class BaseProvider(ABC):
    @abstractmethod
    def list_models(self) -> dict:
        raise NotImplementedError()
    @abstractmethod
    def has_model(self, model : str) -> bool:
        raise NotImplementedError()
    
    @abstractmethod
    def get_comprehension_functions_of(self, model : str) -> list[ComprehensionFunctions] | None:
        raise NotImplementedError()

    @abstractmethod
    def make_question_awnser_call(self, prompt : str, model : str) -> str:
        raise NotImplementedError()
    
    @abstractmethod
    def make_token_classification_call(self, prompt : str, model : str) -> list[dict]:
        raise NotImplementedError()
    
    @abstractmethod
    def make_sentiment_analysis_call(self, prompt : str, model : str) -> list[dict]:
        raise NotImplementedError()

    @abstractmethod
    def make_text_similarity_call(self, text_1 : str, text_2 : str, model : str) -> float:
        raise NotImplementedError()
    # TOKEN_CLASSIFICATION = 1
    # SENTIMENT_ANALYSIS = 2
    # TEXT_SIMILARITY = 3 
    # question_awnser = 4