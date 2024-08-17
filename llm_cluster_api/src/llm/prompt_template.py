from dataclasses import dataclass
from uuid import UUID
import copy

@dataclass
class PromptTemplate:
    template : str
    args : dict
    id : UUID

    @staticmethod
    def __apply_variables(text : str, inputs) -> str:
        variables = []
        for variable in inputs["variables"] or []:
            variables.append([text.find('{'+ variable +'}'), variable])

        variables = sorted(variables)[::-1]


        for _, variable in variables:
            text = text.replace('{'+ variable+ '}', inputs["variables"][variable], 1)

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
