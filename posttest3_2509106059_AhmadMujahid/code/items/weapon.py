from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong
from utils.traits.trait_entry import TraitEntry


class Weapon(EquippableItem):
    def __init__(self, name: str, price: int = 40, traits = None, two_handed: bool = False) -> None:
        slots = {EquipmentSlot.MAIN_HAND}

        if not two_handed:
            slots.add(EquipmentSlot.OFF_HAND)

        super().__init__(name, price, "Senjata petualang", slots, traits)

        self.two_handed = two_handed

    @property
    def occupied_slots(self) -> frozenset:
        if self.two_handed:
            return frozenset({EquipmentSlot.MAIN_HAND, EquipmentSlot.OFF_HAND})

        return frozenset()


class CorosionDagger(Weapon):
    def __init__(self) -> None:
        super().__init__("Corosion Dagger", 40, [TraitEntry(Toxin(), 1)])


class VenomousAxe(Weapon):
    def __init__(self) -> None:
        super().__init__("Venomous Axe", 65, [TraitEntry(Toxin(), 1), TraitEntry(Strong(), 1)])


class GreatSword(Weapon):
    def __init__(self) -> None:
        super().__init__("Great Sword", 120, [TraitEntry(Strong(), 2)], two_handed = True)
