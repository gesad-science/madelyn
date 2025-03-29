from src.llm_providers.base_provider import BaseProvider
from src.exceptions.business_rule_exception import BusinessRuleException
import requests


from src.consts import HUGGINGFACE_BASE_URL, HUGGINGFACE_MODELS, HUGGINGFACE_TOKEN

class HuggingFaceProvider(BaseProvider):

    def __init__(self, base_url = HUGGINGFACE_BASE_URL, models = HUGGINGFACE_MODELS, token = HUGGINGFACE_TOKEN ) -> None:
        self.models = models
        self.base_url = base_url
        self.token = token
        
    def list_models(self) -> list[str]:
        return self.models
    
    def has_model(self, model : str) -> bool:
        return model in self.models

    def make_call(self, prompt : str, model : str) -> str:
        
        if not self.has_model(model):
            raise BusinessRuleException(
                detail=f"HuggingFace provider do not support {model}",
                private=True,
                mask_detail="Unexpected internal Error"
            )
        
        response = requests.post(
                               url=self.base_url + model, 
                               headers={"Authorization": f"Bearer {self.token}"}, 
                               json={
                                     "inputs": prompt, 
                                     "options": {"use_cache": True, "wait_for_model": True}
                                    }
                              )
        
        if not response.ok:           
            raise BusinessRuleException(
                        detail= f'From HuggingFace: {response.json()["error"]}', 
                        private=  True,
                        mask_detail="The server cant connect to the llm provider right now"
                    )
    
        return response.json()[0]['generated_text']

