from src.exceptions.business_rule_exception import BusinessRuleException

from src.llm_providers.base_provider import BaseProvider
import requests


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

    def __init__(self, base_url):

        self.base_url = base_url

        print("pulling")

        for model in ['llama3', 'phi3']:
            self.__pull_model(model)

        print("ended")



    def list_models(self) -> str:
        print("HAHAHA")
        response = requests.get(self.base_url + '/api/tags')
        if not response.ok:
            raise BusinessRuleException(
                                    detail= f'From Ollama: + {response.json()["error"]}', 
                                    private=True,
                                    mask_detail="The server cant connect to the llm provider right now"
                                    )

        json_res = response.json()

        return [ model['model'] for model in json_res['models'] ]

    def has_model(self, model) -> bool:
        models = self.list_models()
        for m in models:
            if m == model or m.split(':')[0] == model:
                return True

        return False

    def make_call(self, prompt, model) -> str:
        print(self.base_url)
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
