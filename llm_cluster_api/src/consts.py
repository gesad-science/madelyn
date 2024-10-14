import os
from dotenv import load_dotenv

load_dotenv()

ARANGODB_URL = os.environ.get('ARANGODB_URL')
ARANGODB_USERNAME = os.environ.get('ARANGODB_USERNAME')
ARANGODB_PASSWORD = os.environ.get('ARANGODB_PASSWORD')
ARANGODB_COLLECTION_NAME = os.environ.get("ARANGODB_COLLECTION_NAME")
ARANGODB_DATABASE_NAME = os.environ.get("ARANGODB_DATABASE_NAME")