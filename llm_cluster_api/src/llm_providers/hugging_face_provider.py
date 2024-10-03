from src.llm_providers.base_provider import BaseProvider

from src.llm.comprehension_services.comprehension_functions import ComprehensionFunctions
import requests
from src.utils.similarity import cos_sim

from transformers import pipeline
from sentence_transformers import SentenceTransformer

from src.exceptions.business_rule_exception import BusinessRuleException

# from 

#https://huggingface.co/api/tasks
class HuggingFaceProvider(BaseProvider):


        # {
    #     'name' : 'distilbert/distilbert-base-uncased-finetuned-sst-2-english',
    #     'comprehension_functions' : ["SENTIMENT_ANALYSIS"] 
    # },
    # {
    #     'name' : 'vblagoje/bert-english-uncased-finetuned-pos',
    #     'comprehension_functions' : ["TOKEN_CLASSIFICATION"] 
    # },
    # {
    #     "name" : "sentence-transformers/all-MiniLM-L6-v2",
    #     "comprehension_functions": ["TEXT_SIMILARITY"]
    # },
    # {
    #     "name": "google/flan-t5-large",
    #     "comprehension_functions": ["QUESTION_AWNSER"]
    # }


    def __init__(self, base_url, token, required_models : list[dict[str, list[str] | str]]) -> None:
        self.token = token
        self.base_url = base_url
        self.__model_capabilies = dict()
        for model in required_models:
            self.__model_capabilies[model["name"]] = [ComprehensionFunctions(x) for x in model["comprehension_functions"]]


    def __assemble_base_request(self, prompt, model):
        return { 
                "json" : {"inputs": prompt, "options": {"use_cache": True, "wait_for_model": True}},
                "headers":{"Authorization": f"Bearer {self.token}"}
               }

    def get_comprehension_functions_of(self, model : str) -> list[ComprehensionFunctions] | None:
        return self.__model_capabilies.get(model, None)

    def list_models(self) -> dict:
        return [ {"name" : x, "comprehension_functions" : self.__model_capabilies[x]} for x in self.__model_capabilies] 
        
    def has_model(self, model : str) -> bool:
        return model in self.__model_capabilies
    
    def make_question_awnser_call(self, prompt : str, model : str) -> str:
        if ComprehensionFunctions.QUESTION_AWNSER not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do question awnser")
        
        response = requests.post(f"{self.base_url}/models/{model}", **self.__assemble_base_request(prompt, model))
        if not response.ok:
            raise BusinessRuleException(detail=f"From hugging face interface: {response.json()}", private = True, mask_detail="Can't connect to hugging face LLM provider")
        
        return response.json()

    def make_token_classification_call(self, prompt : str, model : str) -> list[dict]:
        if ComprehensionFunctions.TOKEN_CLASSIFICATION not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do token classification")
        

        # return {"hii" : "omg hii"}
        ans = pipeline("token-classification", model=model)(prompt)
        for element in ans:
            element["score"] = element["score"].item() 

        return ans
    
    def make_sentiment_analysis_call(self, prompt : str, model : str) -> list[dict]:
        if ComprehensionFunctions.SENTIMENT_ANALYSIS not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do token sentiment analysis")
        
        return pipeline("sentiment-analysis", model=model)(prompt)

    def make_text_similarity_call(self, text_1 : str, text_2 : str, model : str) -> float:
        if ComprehensionFunctions.TEXT_SIMILARITY not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do text similarity")
        
        parsed = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2').encode([text_1, text_2])

        return cos_sim(parsed[0], parsed[1])