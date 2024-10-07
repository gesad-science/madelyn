from dataclasses import dataclass
from typing import Callable, Optional
from uuid import UUID

from validations import * 
from treatments import *

from ..llm_cluster_api.src.db.arango_qa_model_storage import ArangoQAModelStorage
from ..llm_cluster_api.src.llm.LLModelQA import LLModelQA
from copy import deepcopy


@dataclass
class Treatmentinput:
    key : str
    value : str
    processed_atts : dict[str, str]
    prompt_id : UUID
    

    # Passing here the name of the desired model if it is needed
    model_name : Optional[str]

    #not defined yet

    user_input : str
    current_entity : Optional[str]

#########################


@dataclass
class PromptValidation:

    # A exclusive identifier to the PromptValidation
    prompt_validation_id : int

    # The name of the PromptValidation
    name : str

    # A description about the PromptValidation
    description : Optional[str] = None

    operation : Callable[[Treatmentinput],bool]

class PromptValidationCenter:

    # A list where all PromptValidations are going to be registered
    PromptValidations : list[PromptValidation] = [
            PromptValidation(prompt_validation_id=1, name='length_validation', description='checks if the answer size is greater than 0', operation=len_test),
            PromptValidation(prompt_validation_id=2, name='key_equal_value_validation', description='checks if the answer is equal to the key', operation=key_test),
            PromptValidation(prompt_validation_id=3, name='and_validation', description='checks if the answer contains an addition mark', operation=and_test),
            PromptValidation(prompt_validation_id=4, name='att_validation', description='checks if the answer is equal to some processed key', operation=att_test),
            PromptValidation(prompt_validation_id=5, name='pronoun_validation', description='checks if there is an addition mark following a pronoun', operation=pronoun_test),
            PromptValidation(prompt_validation_id=6, name='entity_validation', description='checks if the answer is equal to the entity found', operation=entity_test),
            PromptValidation(prompt_validation_id=7, name='ignoring_validation', description='checks if the answer is ignoring some important information', operation=ignoring_test),
            PromptValidation(prompt_validation_id=8, name='float_validation', description='checks if the wanted value is a float value, and then discover if the model correctly find the value or only the integer part', operation=float_test),
            PromptValidation(prompt_validation_id=9, name='char_validation', description='checks if the answer has some noise characters', operation=char_test)
    ]


    @classmethod
    def get_validation_by_id(cls, id : int) :
        for pv in cls.PromptValidations:
            if pv.prompt_validation_id == id:
                return pv
        return None

@dataclass
class Treatment:

    # A exclusive identifier to the treatment
    treatment_id : int

    # The name of the treatment
    name : str

    # A description about the treatment
    description : Optional[str] = None

    operation : Callable[[Treatmentinput],Treatmentinput]

class TreatmentCenter:

    # A list where all treatments are going to be registered
    treatments : list[Treatment] = [
        Treatment(treatment_id=2, name='new_request_treatment', description='A flag to indicate to the system to execute the treatments', operation=request_new_answer)
    ]

    # List of treatments that are made every tive before the regular ones
    mandatory_treatments : list[Treatment] = [
        Treatment(treatment_id=1, name='similarity_filter', description='This treatment gets the interception between the response from the model and the user input', operation=similarity_filter)
    ]

    """ 
        This is suposed to store the every pipeline of treatment
    
        Example:

        {
            "where_clause_pipeline" : (
                                    [where_clause_treatment_1, where_clause_treatment_2, where_clause_treatment_3], <- list of treatments that are going to run in this pipeline
                                    [where_clause_validation, default_validation] <- list of validators that are going to evaluate the treatments output
            
            ),

            "att_pipeline" : (...)
        }   
    """
    treatment_lines : dict[str, tuple[ list[Treatment], list[PromptValidation]  ]]

    @classmethod
    def get_treatment_by_id(cls, id : int):

        for mt in cls.mandatory_treatments:
            if mt.treatment_id == id:
                return mt
        for tr in cls.treatments: 
            if tr.treatment_id == id:
                return tr
        return None
    
    @classmethod
    def run_validations(cls, input : Treatmentinput, validations : list):

        ok = True # Flag to show if the input passed in all if its validations

        for validation in validations:
            if not validation.operation(input):
                ok = False
                break

        return ok

    @classmethod
    def run_prompt_treatments(cls, input : Treatmentinput, model : LLModelQA):
        for prompt in model.list_prompts()['prompt_alternatives_uid']:
            input.prompt_id = prompt
            answer = request_new_answer(input=input)
            answer = cls.run_mandatory_treatments(answer)
            if cls.run_validations(answer):
                return answer
        return None


    @classmethod
    def run_mandatory_treatments(cls, input : Treatmentinput):
        for treatment in cls.mandatory_treatments:
            input = treatment(input)
        return input


    @classmethod
    def run_line(cls, line_name : str, input : Treatmentinput):

        treatments, validations = cls.treatment_lines[line_name]
        
        # executing mandatory treatments
        input = cls.run_mandatory_treatments(input)
        
        # executing regular treatments and validations for each model
        for model in ArangoQAModelStorage.list_models():

            # Making a deepcopy just to be sure that any treatment made with model A
            # is passed to model B input 
            input_ = deepcopy(input)
            input_.model_name = model['name']

            # Adding None at the end of the treatments so it repeat one more that
            # to validate the last treatment changes
            for treatment in treatments + [None]:
                if input_:
                    if cls.run_validations(input=input_, validations=validations):
                        return input_
                    if treatment.name== 'new_request_treatment':
                        input_ = cls.run_prompt_treatments(input=input, model=model)
                        if cls.run_prompt_treatments is not None:
                            return input_
                    elif treatment is not None:
                        input_ = treatment.operation(input) 
                        input_ = cls.run_mandatory_treatments(input_) # executing mandatory treatments for the new input.

        

        # Just returned it because dont really know what to do when nothing goes right 
        return input