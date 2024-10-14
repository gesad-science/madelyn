from fastapi import FastAPI, status, Response, HTTPException
from src.query_router import query_router


tags_metadata = [
    {"name": "Query"},
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(query_router)

