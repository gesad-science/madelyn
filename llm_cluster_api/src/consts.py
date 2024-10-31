import os
from dotenv import load_dotenv

load_dotenv()

ARANGODB_URL = os.environ.get('ARANGODB_URL')
ARANGODB_USERNAME = os.environ.get('ARANGODB_USERNAME')
ARANGODB_PASSWORD = os.environ.get('ARANGODB_PASSWORD')
ARANGODB_COLLECTION_NAME = os.environ.get("ARANGODB_COLLECTION_NAME")
ARANGODB_DATABASE_NAME = os.environ.get("ARANGODB_DATABASE_NAME")

OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')

HUGGINGFACE_BASE_URL = os.environ.get("HUGGINGFACE_BASE_URL", "https://api-inference.huggingface.co/models/") 
HUGGINGFACE_TOKEN = "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"

OLLAMA_MODELS = ['mistral', 'llama3', 'phi3']
HUGGINGFACE_MODELS = ["google/flan-t5-small"] 
