from entities import Treatmentinput
from ..llm_cluster_api.src.llm.LLModelQA import LLModelQA
from ..llm_cluster_api.src.llm.comprehension_services.question_awnser_service import QuestionAwnserService
from ..llm_cluster_api.src.db.arango_qa_model_storage import ArangoQAModelStorage
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

def cleaning_treatment(input : Treatmentinput) -> Treatmentinput:
    input.value = re.sub(r'^\s+|\s+$', '', input.value)
    return input

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

def request_new_answer(input : Treatmentinput) -> Treatmentinput:

    return QuestionAwnserService.make_call(prompt_uid=input.prompt_id, 
                                           inputs={
                                               "variables":{
                                                'entity' : input.current_entity, 
                                                'user_msg' : input.user_input,
                                                'attribute_key' : input.key,
                                                'attribute_value' : input.value
                                                }
                                            }, 
                                           model_name=input.model_name)

def string_and_treatment(input : Treatmentinput) -> Treatmentinput:

    if input.prompt_id:
        return input

    user_msg = input.user_input
    key = input.key

    # getting everything after the attribute key and before an addition marker
    fragment_short = user_msg[user_msg.find(key) + len(key):]
    fragment_short = user_msg.split(',')[0]
    fragment_short = fragment_short.split(' and ')[0]

    input.value = fragment_short

    return input

def string_noise_treatment(input : Treatmentinput) -> Treatmentinput:

    if input.prompt_id:
        return input

    user_msg = input.user_input
    key = input.key

    fragment_short = user_msg[user_msg.find(key) + len(key):]
    fragment_short = fragment_short.replace('=', '').replace("'", '').replace('"', '').replace('\n', '')

    input.value = fragment_short

    return input

 

