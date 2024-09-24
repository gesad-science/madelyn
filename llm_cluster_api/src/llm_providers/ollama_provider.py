from src.exceptions.business_rule_exception import BusinessRuleException
from src.llm.llm_capabilities import LLMCapabilities
from src.llm_providers.base_provider import BaseProvider
import requests

from src.utils.similarity import cos_sim

class OllamaProvider(BaseProvider):

    __MASK_ERROR__ = "The server cant connect to the llm provider right now"

    def __pull_model(self, model_name : str):
        response = requests.post(f"{self.base_url}/api/pull", json={"name" : model_name, "stream": False})
        if not response.ok:
            raise BusinessRuleException(
                                    detail= f'From Ollama: {response.json()["error"]}', 
                                    private=True,
                                    mask_detail= self.__MASK_ERROR__
                                    )

    def __init__(self, base_url : str, required_models : list[dict[str, list[str] | str]]):

        self.base_url = base_url

        self.__model_capabilies = dict()

        for model in required_models:
            self.__pull_model(model["name"])
            self.__model_capabilies[model["name"]] = [LLMCapabilities(x) for x in model["capabilities"]]

    def capabilities_of(self, model: str) -> list[LLMCapabilities] | None:
        return self.__model_capabilies.get(model, None) 

    def list_models(self) -> str:
        response = requests.get(self.base_url + '/api/tags')
        if not response.ok:
            raise BusinessRuleException(
                                    detail= f'From Ollama: + {response.json()["error"]}', 
                                    private=True,
                                    mask_detail=self.__MASK_ERROR__
                                    )

        json_res = response.json()

        return [ {"name" : model['model'] , "capabilities" : self.__model_capabilies[model["model"]] } for model in json_res['models'] ]

    def has_model(self, model) -> bool:
        models = self.list_models()
        for m in models:
            if m == model or m.split(':')[0] == model:
                return True

        return False

    def make_question_awnser_call(self, prompt, model) -> str:
        if LLMCapabilities.QUESTION_AWNSER not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do question awnser")

        response = requests.post(self.base_url + '/api/generate',
                                headers = { "Content-Type": "application/json" },
                                json={
                                    'prompt': prompt,
                                    'model': model,
                                    'stream': False,
                                }
                               )

        if not response.ok:
            raise BusinessRuleException(
                                        detail= f'From Ollama: + {response.json()["error"]}', 
                                        private=  True,
                                        mask_detail="The server cant connect to the llm provider right now"
                                       )
        
        return response.json()['response']
        

    def make_text_similarity_call(self, text_1 : str, text_2 : str, model : str) -> bool:
        if LLMCapabilities.TEXT_SIMILARITY not in self.__model_capabilies[model]:
            raise BusinessRuleException(detail=f"Model {model} cant do text similarity")
        response = requests.post(f"{self.base_url}/api/embed", json={"model": model,  "input": [text_1, text_2], "stream" : False})

        if not response.ok:
            raise BusinessRuleException(detail=f"From Ollama: {response.json()}", private = True, mask_detail="Can't connect to Ollama LLM provider")

        parsed = response.json()["embeddings"]

        return cos_sim(parsed[0], parsed[1])


    def make_token_classification_call(self, prompt : str, model : str) -> dict:
        raise BusinessRuleException(detail=f"Model {model} cant handle token classification", private=True, mask_detail="There is no implemented way to call an ollama model to do token classification")
    def make_sentiment_analysis_call(self, prompt : str, model : str) -> dict:
        raise BusinessRuleException(detail=f"Model {model} cant handle sentiment analysis", private=True, mask_detail="There is no implemented way to call an ollama model to do sentiment analysis")
