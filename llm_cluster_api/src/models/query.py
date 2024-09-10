from pydantic import BaseModel
from uuid import UUID

class Query(BaseModel):
    variables : dict[str, str]
    prompt_uid : UUID | None = None
