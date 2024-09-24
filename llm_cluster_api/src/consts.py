import os
from dotenv import load_dotenv

load_dotenv()

ARANGODB_URL = os.environ.get('ARANGODB_URL')
ARANGODB_USERNAME = os.environ.get('ARANGODB_USERNAME')
ARANGODB_PASSWORD = os.environ.get('ARANGODB_PASSWORD')
ARANGODB_COLLECTION_NAME = os.environ.get("ARANGODB_COLLECTION_NAME")
ARANGODB_DATABASE_NAME = os.environ.get("ARANGODB_DATABASE_NAME")

OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL')

OLLAMA_MODELS = [
    {
        'name' : 'llama3',
        'capabilities' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    },
    {
        'name' : 'phi3',
        'capabilities' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    }
]


HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")
HUGGING_FACE_BASE_URL = os.environ.get("HUGGING_FACE_BASE_URL")
HUGGING_FACE_MODELS = [
    {
        'name' : 'llama3',
        'capabilities' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    },
    {
        'name' : 'phi3',
        'capabilities' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    }
]