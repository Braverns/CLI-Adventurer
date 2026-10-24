from utils.traits.trait import Trait

class StatsTrait(Trait):
    def __init__(self, name: str, description: str, icon: str, max_stack: int, target: str, value: float | int) -> None:
        super().__init__(name, description, icon, max_stack) 
        self.target = target
        self.__value = value

    def get_effect(self, stack: int) -> dict:
        effect = {"max_stack": self.max_stack, "target": self.target, "value": self.__value * stack}
        return effect
    
    def apply(self, character, amount: int) -> None:
        current_value = getattr(character.stats, self.target)
        effect = self.get_effect(amount)
        setattr(character.stats, self.target, current_value + effect["value"])

    def remove(self, character, amount: int) -> None:
        current_value = getattr(character.stats, self.target)
        effect = self.get_effect(amount)
        setattr(character.stats, self.target, current_value - effect["value"])

    def on_add(self, character, amount: int) -> None:
        self.apply(character, amount)

    def on_remove(self, character, amount: int) -> None:
        self.remove(character, amount)


class Strong(StatsTrait):
    def __init__(self) -> None:
        teks: str = "Kuat"
        super().__init__(name = "Strong", description = teks, icon = "", max_stack = 20, target = "strength", value = 5)



