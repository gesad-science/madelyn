from .entities import Treatmentinput
from ..services import qa_service, token_classification_service
from src.config import QA_SERVICE_URL

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
    fragment_short = clean_string(fragment_short)
    fragment_short = ' ' + fragment_short.strip() + ' '
    answer_list = []

    for word in words: # assembling the answer
        if len(word)>0 and word != '=':

            clean_word = ' ' + word[1:-1].replace('\n', '') + ' '
            single_word = ' ' + word.replace('\n', '') + ' '
            reduced_word = ' ' + word[1:-1] + ' '
            dry_word = ' ' + clean_string(word) + ' '
            candidates = [clean_word, single_word, reduced_word, word, dry_word]

            for candidate in candidates:
                if candidate in fragment_short:
                    if candidate not in answer_list:
                        answer_list.append(candidate.strip())
                        break
    final_answer = ''
    if len(answer_list)>0:
        final_answer = ' '.join(answer_list)
    input.value = final_answer.strip()

    return input

def request_new_answer(input : Treatmentinput) -> Treatmentinput:

    fragment_short_idx = input.user_input.find(input.key)
    fragment_short = input.user_input[fragment_short_idx+len(input.key)]

    response = qa_service(variables={"entity" : input.current_entity, 
                                                "user_msg" : input.user_input,
                                                "attribute_key" : input.key,
                                                "fragment_short" : fragment_short,
                                                "user_intent" : input.current_intent}, 
                                 model_name=input.model_name,
                                 prompt_type='attribute')
    input.value = response['data']['response']
    return input

def entity_filter(input : Treatmentinput) -> Treatmentinput:

    words = input.value.split(' ')
    words = list(filter(lambda x: x != '', words))
    candidates = []
    for word in words:
        word = clean_string(word)
        single_word = ' ' + word.lower() + ' '
        if single_word in input.user_input:
            candidates.append(single_word.strip())

    if not candidates:
        for word in words:
            if word.lower() in input.user_input:
                candidates.append(word.strip())
    candidates_str = ' '.join(candidates)
    tokens = token_classification_service(candidates_str)
    for token in tokens:
        if token['entity'] == 'NOUN':
            input.value = token['word']
            return input
        

def clean_string(string : str) -> str:
    return string.replace('\n', '').replace('=', '').replace(',', '').replace('.', '') 




