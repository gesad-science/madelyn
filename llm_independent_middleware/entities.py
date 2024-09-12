from dataclasses import dataclass
from typing import Callable, Optional
from uuid import UUID

@dataclass
class Treatmentinputs:
    key : str
    value : str
    processed_atts : dict[str, str]
    prompt_id_list : list[UUID]

#########################


@dataclass
class Treatment:

    # A exclusive identifier to the treatment
    treatment_id : int

    # The name of the treatment
    name : str

    # A description about the treatment
    description : Optional[str] = None

    operation : Callable[[Treatmentinputs, LLModel],Treatmentinputs]

class TreatmentCenter:

    # A list where all treatments are going to be registered
    Treatments : list[Treatment]

    # List of treatments that are made every tive before the regular ones
    mandatory_treatments : list[Treatment]

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
    treatment_lines : dict[str, tuple[ list[TreatmentId], list[PromptValidationId]  ]]


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
    PromptValidations : list[PromptValidation]
