from pydantic import BaseModel

from src.models.prompt import Prompt

class Model(BaseModel):
    name : str
    main_prompt : Prompt
    prompt_variaitons : list[Prompt] = []
    validations : list[int] = []
    