from utils.traits.trait import Trait

class ResourceTrait(Trait):
    def __init__(self, name: str, max_stack: int, description: str, icon: str, effect: dict) -> None:
        super().__init__(name, description, icon, max_stack)
        self.base_effect = effect

    def get_effect(self, stack: int) -> dict:
        effect = {}
        for key, value in self.base_effect.items():
            effect[key] = value * stack

        return effect
        

class LuckiestAdventurer(ResourceTrait):
    def __init__(self) -> None:
        teks: str = "Beruntung"
        super().__init__(name = "Luckiest Adventurer", max_stack = 5, 
                         description = teks, icon = "", 
                         effect = {"bonus_gold": 10, "equipment_chance": 0.1})

    def apply(self, character, stack: int) -> None:
        current_gold = getattr(character, "gold")
        effect = self.get_effect(stack)
        setattr(character, "gold", current_gold + effect["bonus_gold"])

    def on_reward(self, character, stack: int) -> None:
        self.apply(character, stack)



