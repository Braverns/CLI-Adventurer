from items.item import Item
from typing import TYPE_CHECKING

from utils.traits.trait_entry import TraitEntry
from utils.traits.trait_entry import TraitEntry
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong


class Weapon(Item):
    def __init__(self, name: str, traits: list[TraitEntry]) -> None:
        super().__init__(name)
        self.traits = traits


class CorosionDagger(Weapon):
    def __init__(self) -> None:
        super().__init__("Corosion Dagger", [TraitEntry(Toxin(), 1)])

class VenomousAxe(Weapon):
    def __init__(self) -> None:
        super().__init__("Venomous Axe", [TraitEntry(Toxin(), 1), TraitEntry(Strong(), 1)])
        
        
