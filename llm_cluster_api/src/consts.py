import os
from dotenv import load_dotenv

load_dotenv()

COUCHDB_URL = os.environ.get('COUCHDB_URL')
COUCHDB_USERNAME = os.environ.get('COUCHDB_USERNAME')
COUCHDB_PASSWORD = os.environ.get('COUCHDB_PASSWORD')
COUCHDB_DATABSE_NAME = os.environ.get('COUCHDB_DATABASE_NAME')




OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')

HUGGINGFACE_BASE_URL = os.environ.get("HUGGINGFACE_BASE_URL", "https://api-inference.huggingface.co/models/") 
HUGGINGFACE_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

OLLAMA_MODELS = ['mistral', 'llama3', 'phi3']
HUGGINGFACE_MODELS = ["google/flan-t5-small"] 
