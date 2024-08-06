from fastapi import HTTPException
from src.providers.base_provider import BaseProvider
import requests

class OllamaProvider(BaseProvider):

    def __init__(self, base_url):
        self.base_url = base_url

    def list_models(self) -> str:
        response = requests.get(self.base_url + '/api/tags')
        if not response.ok:
            raise HTTPException(
                    status_code=response.status_code,
                    detail= response.json()['error']
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
            raise HTTPException(
                                status_code=response.status_code,
                                detail= "From provider: " + response.json()['error'] 
                               )
        
        return response.json()['response']
