from pydantic import BaseModel
from uuid import UUID

class Prompt(BaseModel):
    template: str
    agrs : dict