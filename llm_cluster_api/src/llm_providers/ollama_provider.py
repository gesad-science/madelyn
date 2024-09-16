from src.exceptions.business_rule_exception import BusinessRuleException

from src.llm_providers.base_provider import BaseProvider
import requests

from ollama import Client

class OllamaProvider(BaseProvider):

    def __init__(self, base_url):

        self.base_url = base_url

        c = Client(host=base_url)

        print("pulling")

        c.pull("llama3")
        c.pull("phi3")

        print("pulling ended")

    def list_models(self) -> str:
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
