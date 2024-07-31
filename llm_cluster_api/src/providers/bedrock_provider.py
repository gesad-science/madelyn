from fastapi import HTTPException
import requests, os
from src.providers.base_provider import BaseProvider

class BedrockProvider(BaseProvider):

    def has_model(self, model) -> bool:
        raise NotImplementedError

    def make_call(self, prompt, model) -> str:
        raise NotImplementedError
    
    def list_models(self) -> str:
        raise NotImplementedError