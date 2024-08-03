from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable

from src.llm.LLModel import LLModel

from src.llm.validation_functions.validate_variables import validate_variables
from src.llm.prompt_template import PromptTemplate

from uuid import UUID

class QueryValidator(ABC):

    ################################################################
    @dataclass
    class ValidationTemplate:                         
        id : int
        # args : dict
        validation_name : str
        validation_description : str
        """
            The validation function receive the arguments
            str : prompt template
            dict : template inputs
            dict : validation base args
        """
        validation_funciton : Callable[ [str,dict,dict] , bool]
    ################################################################


    __validations = [
        ValidationTemplate(
            id=0,
            validation_name="Check prompt variable",
            validation_description="It receive as args a list with all variable names and uses to check ",
            validation_funciton= validate_variables
        ),
    ]

    @abstractmethod   
    def validate(self, query_data: dict):
        raise NotImplemented("Subclass should implement this")


    def validate(self, prompt_id: UUID, inputs : dict, model : LLModel):
        raise NotImplemented("Subclass should implement this")

    @abstractmethod
    def add_validator_to_model(validation_function) -> None:
        raise NotImplemented("Subclass should implement this")
                   
 