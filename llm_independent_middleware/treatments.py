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

def similarity_filter(input : Treatmentinput) -> Treatmentinput:

    words = input.value.split(' ')
    words = list(filter(lambda x: x != '', words))
    fragment_short = ' ' + input.user_input[input.user_input.find(input.key) + len(input.key):] + ' '
    #fragment_short = fragment_short.replace('=', ' ').replace(',', ' ').replace('.', ' ')

    answer_list = []

    for word in words: # assembling the answer
        if len(word)>0:

            clean_word = ' ' + word[1:-1].replace('\n', '') + ' '
            single_word = ' ' + word.replace('\n', '') + ' '
            reduced_word = word[1:-1]
            dry_word = word.replace('=', '').replace(',', '').replace('.', '')

            candidates = [clean_word, single_word, reduced_word, word, dry_word]

            for candidate in candidates:
                if candidate in fragment_short:
                    if candidate not in answer_list:
                        answer_list.append(candidate)
                        break

    if len(answer_list)>0:
        final_answer = ' '.join(answer_list)

    input.value = final_answer

    return input


            

