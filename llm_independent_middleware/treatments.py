from entities import Treatmentinput
from madelyn.llm_cluster_api.src.llm.LLModel import LLModel

def intent_filter(input : Treatmentinput, model : LLModel) -> Treatmentinput:

    value = input.value

    options = [' Yes ', ' No ', ' CREATE ', ' READ ', ' UPDATE ', ' DELETE ']
    for option in options:
        if option in value:
            return re.sub(r'^\s+|\s+$', '', option)
            
        #trying to find anyway

        for option in options:
            if re.sub(r'^\s+|\s+$', '', option) in value:
                return re.sub(r'^\s+|\s+$', '', option)
        return None