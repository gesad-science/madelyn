from dataclasses import dataclass
from uuid import UUID

@dataclass
class PromptTemplate:
    template : str
    args : dict
    id : UUID