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
        Treatment(name='extract_entity', description='Searchs for the first noun in the user message', operation=extract_entity),
        Treatment(name='extract_attribute', description='Gets the word following the attribute key in the message', operation=extract_attribute)
    ]

    # List of treatments that are made every tive before the regular ones
    mandatory_treatments : list[Treatment] = [
        Treatment(name='similarity_filter', description='This treatment gets the interception between the response from the model and the user input', operation=similarity_filter),
        Treatment(name='entity_filter', description='This treatment gets the first interception between the response from the model and the user input. it returns a single word as response', operation=entity_filter),
        Treatment(name='intent_filter', description='Extracts the exact intent string from the model response', operation=intent_filter),
        Treatment(name='filter_filter', description='Searchs for an processed attribute key in the model response', operation=find_filter)
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
    # mandatory treatments, regular treatments and validations
    treatment_lines : dict[str, tuple[ list[Treatment], list[Treatment], list[PromptValidation]  ]] = {'attributes_pipeline' : ([mandatory_treatments[0]],[treatments[1]],PromptValidationCenter.PromptValidations),
                                                                                      'entity_pipeline' : ([mandatory_treatments[1]], [treatments[0]], [PromptValidationCenter.PromptValidations[0],PromptValidationCenter.PromptValidations[9]]),
                                                                                      'intent_pipeline' : ([mandatory_treatments[2]], [], []),
                                                                                      'filter_pipeline' : ([mandatory_treatments[3]], [], [])
                                                                                      }
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

        if validations:
            for validation in validations:
                if not validation.operation(input):
                    ok = False
                    break
        return ok

    @classmethod
    def run_mandatory_treatments(cls, treatments : list, input : Treatmentinput):
        for treatment in treatments:
            input = treatment.operation(input)
        return input


    @classmethod
    def run_line(cls, line_name : str, input : Treatmentinput):
        mandatory_treatments, treatments, validations = cls.treatment_lines[line_name]
        # executing mandatory treatments
        input = cls.run_mandatory_treatments(treatments=mandatory_treatments, input=input)

        if not input.complete_treatment:
            return input

        # Making a deepcopy just to be sure that any treatment made with model A
        # is passed to model B input 
        input_ = deepcopy(input)

        # Adding None at the end of the treatments so it repeat one more that
        # to validate the last treatment changes
        for treatment in treatments + [None]:

            if input_:

                if cls.run_validations(input=input_, validations=validations):
                    input_.acceptable_answer = True
                    return input_
                
                if treatment:
                    input_ = treatment.operation(input) 
                    input = cls.run_mandatory_treatments(treatments=mandatory_treatments, input=input_) # executing mandatory treatments for the new input.

        # Just returned it because dont really know what to do when nothing goes right 
        input.acceptable_answer = False
        return input