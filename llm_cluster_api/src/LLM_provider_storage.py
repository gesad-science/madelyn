from src.exceptions.business_rule_exception import BusinessRuleException
from src.llm_providers.hugging_face_provider import HuggingFaceProvider
from src.llm_providers.ollama_provider import OllamaProvider
from src.llm_providers.base_provider import BaseProvider
from abc import ABC


from src.consts import OLLAMA_BASE_URL, OLLAMA_MODELS, HUGGING_FACE_MODELS, HUGGING_FACE_BASE_URL, HUGGING_FACE_TOKEN

class LLMProviderStorage(ABC):
    __providers : dict[str, BaseProvider] = {
        # 'bedrock' : BedrockProvider(),
        'ollama' : OllamaProvider( base_url= OLLAMA_BASE_URL, required_models= OLLAMA_MODELS),
        'hugging_face' : HuggingFaceProvider(base_url= HUGGING_FACE_BASE_URL, token=HUGGING_FACE_TOKEN, required_models=HUGGING_FACE_MODELS),
    }

    __default = 'ollama'

    # @staticmethod
    @classmethod
    def get_provider(cls, provider_name):
        return cls.__providers[provider_name]
    
    @classmethod
    def set_default_provider(cls, default : str):
        cls.__default = default
    
    @classmethod
    def get_default_provider(cls) -> BaseProvider:
        return cls.get_provider(cls.__default)
    
    @classmethod
    def get_provider_with_model(cls, model : str):
        for provider in cls.__providers.values():
            if provider.has_model(model):
                return provider
        raise BusinessRuleException(f"Cant find {model} in any model provider")
    
    @classmethod
    def list_all_models(cls):
        model_names = set()
        model_list = list()

        for provider in cls.__providers.values():
            print(provider)

            for model in provider.list_models():
                if model['name'] not in model_names:
                    model_names.add(model['name'])
                    model_list.append(model)
        return list(model_list)

    @classmethod
    def has_model(cls, model : str):
        for provider in cls.__providers.values():
            if provider.has_model(model):
                return True
        return False