from src.llm.LLModel import PromptType
from pydantic import BaseModel
from uuid import UUID

class Query(BaseModel):
    variables : dict[str, str]
    prompt_type : PromptType
