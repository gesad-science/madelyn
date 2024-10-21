from fastapi import FastAPI, status, Response, HTTPException
from dotenv import load_dotenv

from src.routers.prompts_router import prompts_router
from src.routers.models_router import models_router
from src.routers.validations_router import validations_router
from src.routers.interpretation_router import interpretation_router

tags_metadata = [
    {"name": "Model"},
    {"name": "Prompt"},
    {"name": "Validation"},
    {"name": "Query"},
]

app = FastAPI(openapi_tags=tags_metadata)
# app.include_router(verificationm_router)
app.include_router(prompts_router)
app.include_router(models_router)
app.include_router(validations_router)
app.include_router(interpretation_router)


"""

    TODO:   
        - Data verifications over paramethers passed from body | OK

        - Assert validation numbers to be in the correct range (for delete and post endpoints) | OK 

        - Adjust redundancy in query endpoint | OK

"""