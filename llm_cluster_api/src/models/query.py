from pydantic import BaseModel
from uuid import UUID
from src.llm.comprehension_services.comprehension_functions import ComprehensionFunctions

class QueryQA(BaseModel):
    variables : dict[str, str]
    prompt_uid : UUID | None = None
    model_name : str


class QueryComprehension(BaseModel):
    func : ComprehensionFunctions
    inputs : list[str]
    model_name : str