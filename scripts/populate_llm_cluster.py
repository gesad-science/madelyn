import requests


# Model example
# {
#   "name": "string",
#   "intent": {
#     "default_prompt": {
#       "template": "string",
#       "args": {}
#     },
#     "prompt_alternatives": []
#   },
#   "entity": {
#     "default_prompt": {
#       "template": "string",
#       "args": {}
#     },
#     "prompt_alternatives": []
#   },
#   "attribute": {
#     "default_prompt": {
#       "template": "string",
#       "args": {}
#     },
#     "prompt_alternatives": []
#   },
#   "filter": {
#     "default_prompt": {
#       "template": "string",
#       "args": {}
#     },
#     "prompt_alternatives": []
#   },
#   "validations": []
# }

models = [
    {
    "name": "mistral",
    "intent": {
        "default_prompt": {
        "template": "-QUESTION: What is the type of CRUD operation the user's current message refers to?\n-CONTEXT: The context here is around a chatbot that updates the data model of its system using the messages received from the end user in Natural Language.\n- CRUD: when the user is asking for a CRUD type operation. CRUD operations refers to the four basic operations a software application should be able to perform: Create, Read, Update, and Delete. (v.g.: 'add a student with name=Anderson'; 'for the student with name=Anderson, update the age for 43'; 'get the teachers with name Paulo Henrique.'; etc.)\nSo, answer me what is the type of CRUD operation the user's current message refers to. \nThe user's current message is: '{user_msg}'\n-OPTIONS: CREATE, READ, UPDATE, DELETE",
        "args": {"variables": ["user_msg"]}
        },
        "prompt_alternatives": []
    },
    "entity": {
        "default_prompt": {
        "template": "Identify the referred entity class in the following user request. Return only the entity class name.\nUser request: '{user_msg}'",
        "args": {"variables": ["user_msg"]}
        },
        "prompt_alternatives": []
    },
    "attribute": {
        "default_prompt": {
        "template": "QUESTION: What is the {attribute_key} in the sentence fragment?\nAnswer me with the exact substring of the sentence fragment.\nAnswer me with only the value of the attribute.\nThe answer must be different from {attribute_key}.\n-CONTEXT: This is the user command: {user_msg}.\nThe intent of the user command is #user_intent.\nThe entity class is {entity}. \nThe answer is a substring of {fragment_short}.\n{attribute_key} is the name of a field in the database.\nI'm trying discover the value of the {attribute_key} in the sentence fragment.\nIn another words, complete to me {attribute_key} + ' = ' ?\nAnswer me with only the value of the attribute.",
        "args": {
            "variables" : ["attribute_key", "entity", "user_msg", "fragment_short"]
        }
        },
        "prompt_alternatives": []
    },
    "filter": { "default_prompt": {"template": "","args": {}}, "prompt_alternatives": []},
    "validations": [0]
    }
]

for model in models:
    res = requests.post("http://0.0.0.0:8000/models", json=model)

    print(res.ok, res.status_code, res.json())
