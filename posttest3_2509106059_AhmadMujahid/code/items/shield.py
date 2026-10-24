from __future__ import annotations

from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem

class Shield(EquippableItem):
    def __init__(self, name: str = "Wooden Shield", price: int = 25, traits=None) -> None:
        super().__init__(name, price, "Perlengkapan tangan kiri", {EquipmentSlot.OFF_HAND}, traits)
