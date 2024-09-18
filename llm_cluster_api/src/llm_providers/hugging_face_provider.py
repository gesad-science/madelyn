from src.llm_providers.base_provider import BaseProvider
from transformers import pipeline
from sentence_transformers import SentenceTransformer

class HuggingFaceProvider(BaseProvider):

    @staticmethod
    def provide_sentence_transformer():
        aux = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        def exec_sentence_transformer(text):
            return aux.encode(text, convert_to_tensor=True)
        return exec_sentence_transformer

    __models = {
                "token-classification"  : pipeline(model="vblagoje/bert-english-uncased-finetuned-pos"), 
                "sentiment-analysis" : pipeline("sentiment-analysis"),
                "text-similarity" : provide_sentence_transformer()
                }

    
    @classmethod
    def list_models(cls) -> list[str]:
        return cls.__models[:]
        
    def has_model(cls, model : str) -> bool:
        return model in cls.__models

    def make_call(cls, prompt : str, model : str) -> str:
        return cls.__models[model](prompt)