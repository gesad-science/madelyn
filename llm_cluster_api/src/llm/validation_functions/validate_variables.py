from src.llm.prompt_template import PromptTemplate


"""
Verifies if all variables inside the prompt args are described in inputs
and the other way around
"""
def validate_variables(prompt : PromptTemplate, inputs : dict):
    print(inputs["variables"])
    print(prompt.args["variables"])
    for variable in inputs["variables"]:
        if variable not in prompt.args["variables"]:
            return False
    for variable in prompt.args["variables"]:
        if variable not in inputs["variables"]:
            return False
    return True