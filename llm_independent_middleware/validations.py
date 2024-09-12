from entities import Promptvalidation, Treatmentinput

def validation_by_id(id : int) -> Promptvalidation:
    match id:
        case 1:
            return PromptValidation(prompt_validation_id=1, name='length_validation', description='checks if the answer size is greater than 0', operation=len_test)
        case 2:
            return PromptValidation(prompt_validation_id=2, name='key_equal_value_validation', description='checks if the answer is equal to the key', operation=key_test)
        case 3:
            return PromptValidation(prompt_validation_id=3, name='and_validation', description='checks if the answer contains an addition mark', operation=and_test)
        case 4:
             return PromptValidation(prompt_validation_id=4, name='att_validation', description='checks if the answer is equal to some processed key', operation=att_test)



##############

def len_test(input : Treatmentinput) -> bool:
    value = input.value
    if len(value) <= 0:
        return False
    return True

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