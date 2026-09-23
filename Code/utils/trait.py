# class Trait:
#     pass

# class StatsTrait:
#     pass 

# class BattleTrait:
#     pass

# class ResourceTrait:
#     pass

class TraitsManajer:
    def __init__(self) -> None:
        self.traits = []

    def add_trait(self, trait) -> None:
        self.traits.append(trait)

    def apply_trait(self, trait, player) -> None:
        if isinstance(trait, Strong):
            player.stats.strength += trait.value

    def remove_trait(self, trait, player) -> None:
        if isinstance(trait, Strong):
            player.stats.strength -= trait.value

    

class Strong:
    name: str = "Strong"
    target = "strength"
    value: int = 5

# class Toxin:
#     name: str = "Toxin"
#     chance: float = 0.075
#     duration: int = 3

# class Luckiest_Adventurer:
#     name: str = "Luckiest Adventurer"
#     bonus_gold: int = 10
#     equipment_chance: float = 0.1
