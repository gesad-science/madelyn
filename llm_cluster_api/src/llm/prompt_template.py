from dataclasses import dataclass
from uuid import UUID, uuid4
import copy

@dataclass
class PromptTemplate:
    template : str
    args : dict
    id : UUID

    @staticmethod
    def __apply_variables(text : str, inputs) -> str:
        variables = inputs['variables'] if 'variables' in inputs else {}
    
        var_and_uuid= [(variable, uuid4().__str__()) for variable in variables]

        for variable, uid in var_and_uuid:
            text = text.replace('{'+variable+'}', '{'+uid+'}')

        for variable, uid in var_and_uuid:
            text = text.replace('{'+uid+'}', variables[variable])

        print(text)
        return text

    def apply_input(self, inputs : dict) -> str:
        constructions = [
            self.__apply_variables,
        ]

        text = copy.deepcopy(self.template)
        for function in constructions:
            text = function(text, inputs)
            
        return text
