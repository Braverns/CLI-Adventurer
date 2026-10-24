from core.enums import EquipmentSlot
from items.item import Item

class EquippableItem(Item):
    def __init__(self, name: str, price: int, description: str, allowed_slots, traits=None) -> None:
        super().__init__(name, price, description)
        self.allowed_slots = frozenset(allowed_slots)
        if not self.allowed_slots or not all(isinstance(slot, EquipmentSlot) for slot in self.allowed_slots):
            raise ValueError("Slot equipment tidak valid")
        self.traits = list(traits or [])

    @property
    def occupied_slots(self) -> frozenset:
        return frozenset()

    def can_use_slot(self, slot: EquipmentSlot) -> bool:
        return slot in self.allowed_slots
