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
        error_log : str
        """
            The validation function receive the arguments
            PromptTemplate : the template in question
            dict : inputs
        """
        validation_funciton : Callable[ [PromptTemplate,dict] , bool]
    ################################################################


    __validations = [
        ValidationTemplate(
            id=0,
            validation_name="Check prompt variable",
            validation_description="It receive as args a list with all variable names and uses to check ",
            error_log= "Variables passed dont match the template",
            validation_funciton= validate_variables
        ),
    ]

    @classmethod
    def validate(cls, prompt: PromptTemplate, inputs : dict, validations : list[int]):
        fails_log = []
        for validation_id in validations:
            if not 0 <= validation_id < len(cls.__validations):
                fails_log.append(f"there is no validation with index {validation_id}")
                continue

            if not cls.__validations[validation_id].validation_funciton(prompt, 
                                                                        inputs):
                fails_log.append(cls.__validations[validation_id].error_log)

        return fails_log