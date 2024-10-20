from .entities import Treatmentinput
import requests
from src.config import COMPREHENSION_SERVICE_URL

# from entities import Promptvalidation, Treatmentinput

# def validation_by_id(id : int) -> Promptvalidation:
#     match id:
#         case 1:
#             return PromptValidation(prompt_validation_id=1, name='length_validation', description='checks if the answer size is greater than 0', operation=len_test)
#         case 2:
#             return PromptValidation(prompt_validation_id=2, name='key_equal_value_validation', description='checks if the answer is equal to the key', operation=key_test)
#         case 3:
#             return PromptValidation(prompt_validation_id=3, name='and_validation', description='checks if the answer contains an addition mark', operation=and_test)
#         case 4:
#              return PromptValidation(prompt_validation_id=4, name='att_validation', description='checks if the answer is equal to some processed key', operation=att_test)



##############

def token_classification_service(text : str):
    data = {
        "func": "TOKEN_CLASSIFICATION",
        "inputs": [
            text
        ]
    }
    response = requests.post(COMPREHENSION_SERVICE_URL, json=data)
    return response.json()['data']

def len_test(input : Treatmentinput) -> bool:
    value = input.value
    if value:
        if len(value) <= 0:
            return False
        return True
    return False

def key_test(input : Treatmentinput) -> bool:
    value = input.value
    key = input.key
    if key.lower().strip() == key.lower().strip():
        return False
    return True

def and_test(input : Treatmentinput) -> bool:
    value = input.value
    if ' and ' in value:
        return False
    return True

def att_test(input : Treatmentinput) -> bool:
    value = input.value
    atts = input.processed_atts
    if atts is not None:
        for key in atts.keys():
            if value.lower().strip() == key.lower().strip():
                return False
    return True

def pronoun_test(input : Treatmentinput) -> bool: # should be increased in the future

    tokens = token_classification_service(input.value)

    propn = False
    for token in tokens:  # if there is a pronoun followed by a comma
        if propn == True and token['entity'] == 'PUNCT':
            return False
        if token['entity'] == 'PROPN':
            propn = True
    return True

def entity_test(input : Treatmentinput) -> bool: # should be increased in the future
    entity = input.current_entity
    value = input.value
    if entity:
        if value.lower().strip() == entity.lower().strip():
            return False
        return True
    
def ignoring_test(input : Treatmentinput) -> bool:

    tokens = token_classification_service(input.value)

    key_find = False
    tokens_entity = []
    for token in tokens:  # discovering if it is ignoring relevant attributes
        if token['word'] is not None:
            if token['word'].lower() == input.key.lower() and key_find == False:
                key_find = True
                continue
            if key_find:
                if token['word'].lower() in input.value.lower():
                    break
                tokens_entity.append(token['entity'])

    if 'PROPN' in tokens_entity or 'NUM' in tokens_entity:
        return False
    return True

def float_test(input : Treatmentinput) -> bool:

    tokens = token_classification_service(input.value)

    integer_part = None
    j = 0
    key_find = False
    while j < len(tokens):

        if key_find == False:
            if tokens[j]['word'] == input.key:
                key_find = True
            j += 1
            continue
        
        if tokens[j]['entity'] == 'PUNCT' and j > 0 and j+1<len(tokens):
            if tokens[j + 1]['entity'] == 'NUM' and tokens[j - 1]['entity'] == 'NUM':
                # exists a float number in the original mensage
                integer_part = tokens[j - 1]['word']
                break
        elif tokens[j]['entity'] == 'NUM' and j+1<len(tokens): 
            if tokens[j + 1]['entity'] == 'PUNCT':
                j += 1
                continue
            elif tokens[j]['word'] == input.value:
                return True

        j += 1

    if integer_part is None:
        return True

    if integer_part in input.value and (',' not in input.value and '.' not in input.value):
        return False

    return True

def char_test(input : Treatmentinput) -> bool: # should be increased in the future
    tokens = token_classification_service(input.value)
    potential_value = False
    for token in tokens:  # if there is some "noise character" on the final answer
        if potential_value == True and token['entity'] == 'SYM':
            return False
        if token['entity'] == 'PROPN' or token['entity'] == 'NUM':
            potential_value = True
    return True


