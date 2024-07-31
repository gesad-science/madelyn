from fastapi import FastAPI, status, Response, HTTPException
from typing import Union
from src.providers_storage import providers
from src.models.query_props import QueryProps
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Endpoint to LLM queries
@app.post('/query', status_code=200, tags=['query'])
def query(prop : QueryProps):

    if prop.provider in providers:
        if providers[prop.provider].has_model(prop.model):
            return providers[prop.provider].make_call(prop.prompt, prop.model)
        raise HTTPException(status_code=404, detail=f"{prop.model} is not provided by {prop.provider}")
    raise HTTPException(status_code=404, detail=f"{prop.provider} not found")


# Endpoint to list all registered LLM providers
@app.get('/providers', status_code=200, tags=['providers'])
def provider():
    return list(providers.keys())

# Endpoint to list all LLMs available from every provider
@app.get('/llms', status_code=200, tags=['llms'])
def llm():
    return dict( (provider, providers[provider].list_models()) for provider in providers   )
