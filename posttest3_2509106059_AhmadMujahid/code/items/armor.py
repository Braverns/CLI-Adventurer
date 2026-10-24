from __future__ import annotations

from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong
from utils.traits.trait_entry import TraitEntry

class Armor(EquippableItem):
    def __init__(self, name: str, price: int = 40, traits=None, slot=EquipmentSlot.CHEST) -> None:
        super().__init__(name, price, "Pelindung tubuh", {slot}, traits)

class CorosionSpikeArmor(Armor):
    def __init__(self) -> None:
        super().__init__("Corosion Spike Armor", 60, [TraitEntry(Toxin(), 3)])

class GiantArmor(Armor):
    def __init__(self) -> None:
        super().__init__("Giant Armor", 70, [TraitEntry(Strong(), 2)])
