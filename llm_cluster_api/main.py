from fastapi import FastAPI, status, Response, HTTPException
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Endpoint to LLM queries
@app.post('/query', status_code=200, tags=['query'])
def query(prop):
    pass