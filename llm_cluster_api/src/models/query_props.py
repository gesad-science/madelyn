from pydantic import BaseModel
class QueryProps(BaseModel):
    prompt : str
    model : str
    provider : str
