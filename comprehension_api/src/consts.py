import os
from dotenv import load_dotenv

load_dotenv()

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
]