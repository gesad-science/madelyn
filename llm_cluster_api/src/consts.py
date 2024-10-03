import os
from dotenv import load_dotenv

load_dotenv()

ARANGODB_URL = os.environ.get('ARANGODB_URL')
ARANGODB_USERNAME = os.environ.get('ARANGODB_USERNAME')
ARANGODB_PASSWORD = os.environ.get('ARANGODB_PASSWORD')
ARANGODB_COLLECTION_NAME = os.environ.get("ARANGODB_COLLECTION_NAME")
ARANGODB_DATABASE_NAME = os.environ.get("ARANGODB_DATABASE_NAME")

OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')

OLLAMA_MODELS = [
    {
        'name' : 'llama3',
        'comprehension_functions' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    },
    {
        'name' : 'phi3',
        'comprehension_functions' : ["QUESTION_AWNSER", "TEXT_SIMILARITY"] 
    }
]


HUGGING_FACE_TOKEN = os.environ.get("HUGGING_FACE_TOKEN")
HUGGING_FACE_BASE_URL = os.environ.get("HUGGING_FACE_BASE_URL")
HUGGING_FACE_MODELS = [
    {
        'name' : 'distilbert/distilbert-base-uncased-finetuned-sst-2-english',
        'comprehension_functions' : ["SENTIMENT_ANALYSIS"] 
    },
    {
        'name' : 'vblagoje/bert-english-uncased-finetuned-pos',
        'comprehension_functions' : ["TOKEN_CLASSIFICATION"] 
    },
    {
        "name" : "sentence-transformers/all-MiniLM-L6-v2",
        "comprehension_functions": ["TEXT_SIMILARITY"]
    },
    {
        "name": "google/flan-t5-large",
        "comprehension_functions": ["QUESTION_AWNSER"]
    }
]