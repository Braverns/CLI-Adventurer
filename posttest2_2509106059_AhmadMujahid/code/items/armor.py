from items.item import Item
from typing import TYPE_CHECKING

from utils.traits.trait_entry import TraitEntry
from utils.traits.trait_entry import TraitEntry
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong

class Armor(Item):
    def __init__(self, name: str, traits: list[TraitEntry]) -> None:
        super().__init__(name)
        self.traits = traits

class CorosionSpikeArmor(Armor):
    def __init__(self) -> None:
        super().__init__("Corosion Spike Armor", [TraitEntry(Toxin(), 3)])

class GiantArmor(Armor):
    def __init__(self) -> None:
        super().__init__("Giant Armor", [TraitEntry(Strong(), 2)])