class Trait:
    def __init__(self, name: str, description: str, icon: str, max_stack: int) -> None:
        self.__name = name
        self.description = description
        self.icon = icon
        self.__max_stack = max_stack

    @property
    def name(self) -> str:
        return self.__name

    @property
    def max_stack(self) -> int:
        return self.__max_stack

    def on_add(self, character, amount: int) -> None:
        pass
    def on_remove(self, character, amount: int) -> None:
        pass

    def get_effect(self, stack: int) -> dict:
        effetc = {}
        return effetc
