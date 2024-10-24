import os
from dotenv import load_dotenv

load_dotenv()

COUCHDB_URL = os.environ.get('COUCHDB_URL')
COUCHDB_USERNAME = os.environ.get('COUCHDB_USERNAME')
COUCHDB_PASSWORD = os.environ.get('COUCHDB_PASSWORD')
COUCHDB_DATABSE_NAME = os.environ.get('COUCHDB_DATABASE_NAME')




OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
