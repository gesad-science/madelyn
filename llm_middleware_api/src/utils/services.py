from ..config import COMPREHENSION_SERVICE_URL, QA_SERVICE_URL
import requests

def token_classification_service(text : str):
    data = {
        "func": "TOKEN_CLASSIFICATION",
        "inputs": [
            text
        ]
    }
    response = requests.post(COMPREHENSION_SERVICE_URL, json=data)
    return response.json()['data']
'''
def qa_service(variables : dict, model_name : str, prompt_type : str):

    url = QA_SERVICE_URL + f'/{model_name}/query'

    data = {
    "variables": variables,
    "prompt_type": prompt_type,
    }
    response = requests.post(url, json=data)
    return response.json()
'''
