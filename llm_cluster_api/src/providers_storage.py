from src.providers.base_provider import BaseProvider
from src.providers.ollama_provider import OllamaProvider
from src.providers.bedrock_provider import BedrockProvider

providers : dict[str, BaseProvider] = {
    # 'bedrock' : BedrockProvider(),
    'ollama' : OllamaProvider(),
}