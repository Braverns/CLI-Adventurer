from utils.traits.trait import Trait
from utils.traits.trait_entry import TraitEntry
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.character import Character
    from characters.combatant import Combatant

class TraitManager:
    def __init__(self) -> None:
        self.traits: dict[type[Trait], TraitEntry] = {}

    def add_trait(self, trait: Trait, character: Character, amount: int) -> None:
        trait_type = type(trait)

        if trait_type in self.traits:
            self.traits[trait_type].increase_stack(amount)
        else:
            self.traits[trait_type] = TraitEntry(trait, amount)
            
        entry: TraitEntry = self.traits[trait_type]
        entry.trait.on_add(character, amount)
    

    def remove_trait(self, trait: Trait, character: Character, amount: int) -> None:
        trait_type = type(trait)

        if trait_type not in self.traits:
            raise ValueError("Tidak ada trait semacam itu")
            
        entry: TraitEntry = self.traits[trait_type]
        entry.decrease_stack(amount)
        entry.trait.on_remove(character, amount)

        if entry.stack == 0:
            del self.traits[trait_type]

    def trigger_attack(self, attacker: Combatant, target: Combatant) -> None:
        for trait_entry in self.traits.values():
            method = getattr(trait_entry.trait, "on_attack", None)

            if callable(method):
                method(attacker, target, trait_entry.stack)

    def trigger_reward(self, character: Character) -> None:
        for trait_entry in self.traits.values():
            method = getattr(trait_entry.trait, "on_reward", None)

            if callable(method):
                method(character, trait_entry.stack)


    


    