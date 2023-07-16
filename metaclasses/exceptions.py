from typing import Set


class LoadFileError(Exception):
    def __init__(self, path: str):
        self.message = f"Failed to load file: '{path}'"
        super().__init__(self.message)


class MissingTransformersError(Exception):
    def __init__(self, transformer_type: str, transformers: Set[str]):
        self.message = (
            f"The following mandatory '{transformer_type}' "
            f"transformers were not applied: {transformers}"
        )
        super().__init__(self.message)


class InvalidJsonTypeError(TypeError):
    def __init__(self, json_type: str):
        self.message = f"Failed to validate json type: '{json_type}'."
        super().__init__(self.message)
