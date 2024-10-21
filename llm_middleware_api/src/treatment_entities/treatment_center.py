from copy import deepcopy
from .entities import Treatment, PromptValidation

from .validations import * 
from .treatments import *

class PromptValidationCenter:

    # A list where all PromptValidations are going to be registered
    PromptValidations : list[PromptValidation] = [
            PromptValidation(name='length_validation', description='checks if the answer size is greater than 0', operation=len_test),
            PromptValidation(name='key_equal_value_validation', description='checks if the answer is equal to the key', operation=key_test),
            PromptValidation(name='and_validation', description='checks if the answer contains an addition mark', operation=and_test),
            PromptValidation(name='att_validation', description='checks if the answer is equal to some processed key', operation=att_test),
            PromptValidation(name='pronoun_validation', description='checks if there is an addition mark following a pronoun', operation=pronoun_test),
            PromptValidation(name='entity_validation', description='checks if the answer is equal to the entity found', operation=entity_test),
            PromptValidation(name='ignoring_validation', description='checks if the answer is ignoring some important information', operation=ignoring_test),
            PromptValidation(name='float_validation', description='checks if the wanted value is a float value, and then discover if the model correctly find the value or only the integer part', operation=float_test),
            PromptValidation(name='char_validation', description='checks if the answer has some noise characters', operation=char_test),
            PromptValidation(name='in_msg_test', description='tests if the result is in the user message', operation=in_msg_test)
    ]

class TreatmentCenter:

    # A list where all treatments are going to be registered
    treatments : list[Treatment] = [
        Treatment(name='new_request_treatment', description='A flag to indicate to the system to execute the treatments', operation=request_new_answer)
    ]

    # List of treatments that are made every tive before the regular ones
    mandatory_treatments : list[Treatment] = [
        Treatment(name='similarity_filter', description='This treatment gets the interception between the response from the model and the user input', operation=similarity_filter)
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
    treatment_lines : dict[str, tuple[ list[Treatment], list[PromptValidation]  ]] = {'attributes_pipeline' : ([treatments[0]],PromptValidationCenter.PromptValidations),
                                                                                      'entity_pipeline' : ([], [PromptValidationCenter.PromptValidations[0],PromptValidationCenter.PromptValidations[9]])}
    '''
    @classmethod
    def get_treatment_by_id(cls, id : int):

        for mt in cls.mandatory_treatments:
            if mt.treatment_id == id:
                return mt
        for tr in cls.treatments: 
            if tr.treatment_id == id:
                return tr
        return None
    '''
    
    @classmethod
    def run_validations(cls, input : Treatmentinput, validations : list):

        ok = True # Flag to show if the input passed in all if its validations

        for validation in validations:
            if not validation.operation(input):
                ok = False
                break
        return ok

    @classmethod
    def run_mandatory_treatments(cls, input : Treatmentinput):
        for treatment in cls.mandatory_treatments:
            input = treatment.operation(input)
        return input


    @classmethod
    def run_line(cls, line_name : str, input : Treatmentinput):

        treatments, validations = cls.treatment_lines[line_name]
        
        # executing mandatory treatments
        input = cls.run_mandatory_treatments(input)

        # Making a deepcopy just to be sure that any treatment made with model A
        # is passed to model B input 
        input_ = deepcopy(input)

        # Adding None at the end of the treatments so it repeat one more that
        # to validate the last treatment changes
        for treatment in treatments + [None]:

            if input_:

                if cls.run_validations(input=input_, validations=validations):
                    return input_
                
                if treatment:
                    input_ = treatment.operation(input) 
                    input_ = cls.run_mandatory_treatments(input_) # executing mandatory treatments for the new input.

        # Just returned it because dont really know what to do when nothing goes right 
        return input