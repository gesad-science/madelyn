from entities import Treatmentinput
from ..llm_cluster_api.src.llm.LLModelQA import LLModelQA
from ..llm_cluster_api.src.llm.comprehension_services.question_awnser_service import QuestionAwnserService
import re

'''
def intent_filter(input : Treatmentinput, model : LLModelQA) -> Treatmentinput:

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
'''


