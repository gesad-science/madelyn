from enum import Enum

class LLMCapabilities(Enum):
    TOKEN_CLASSIFICATION = "TOKEN_CLASSIFICATION"
    SENTIMENT_ANALYSIS = "SENTIMENT_ANALYSIS"
    TEXT_SIMILARITY = "TEXT_SIMILARITY" 
    QUESTION_AWNSER = "QUESTION_AWNSER"