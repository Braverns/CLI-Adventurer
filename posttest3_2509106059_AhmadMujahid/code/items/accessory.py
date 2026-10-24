from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem


class Accessory(EquippableItem):
    def __init__(self, name: str = "Traveler Cloak", price: int = 20, traits = None) -> None:
        super().__init__(name, price, "Aksesori perjalanan", {EquipmentSlot.BACK}, traits)
