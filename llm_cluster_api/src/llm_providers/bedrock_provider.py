from exceptions.business_rule_exception import BusinessRuleException
import requests, os
from src.llm_providers.base_provider import BaseProvider

class BedrockProvider(BaseProvider):

    def __init__(self, base_url) -> None:
        self.base_url = base_url
        super().__init__()

    def has_model(self, model) -> bool:
        raise NotImplementedError

    def make_call(self, prompt, model) -> str:
        
        requests.post(f'{self.base_url}/model/{1}/converse')
        raise NotImplementedError
    
    def list_models(self) -> str:
        raise NotImplementedError