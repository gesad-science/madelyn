from dataclasses import dataclass
from typing import Callable, Optional

@dataclass
class Treatmentinput:
    key : str
    value : str
    processed_atts : dict[str, str]
    #prompt_id : UUID
    

    # Passing here the name of the desired model if it is needed
    model_name : Optional[str]

    #not defined yet

    user_input : str
    current_entity : Optional[str]
    current_intent : Optional[str]

#########################


@dataclass
class PromptValidation:

    # A exclusive identifier to the PromptValidation
    #prompt_validation_id : int

    # The name of the PromptValidation
    name : str

    operation : Callable[[Treatmentinput],bool]

    # A description about the PromptValidation
    description : Optional[str] = None


@dataclass
class Treatment:

    # A exclusive identifier to the treatment
    #treatment_id : int

    # The name of the treatment
    name : str

    operation : Callable[[Treatmentinput],Treatmentinput]

    # A description about the treatment
    description : Optional[str] = None
