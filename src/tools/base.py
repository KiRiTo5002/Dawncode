from collections.abc import Callable


class Tool:
    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict,
        function: Callable,
    ):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.function = function

    def to_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    def execute(self, **kwargs):

        return self.function(**kwargs)
