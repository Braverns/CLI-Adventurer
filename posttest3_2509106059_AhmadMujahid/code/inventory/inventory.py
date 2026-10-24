from __future__ import annotations

from content.balance import require_integer
from items.item import Item

class Inventory:
    def __init__(self, max_item: int = 10) -> None:
        require_integer(max_item, "Kapasitas", 1)
        self.max_item = max_item
        self.items: list[Item | None] = [None] * max_item

    def validate_slot(self, slot: int) -> None:
        require_integer(slot, "Slot")
        if slot >= self.max_item:
            raise IndexError("Slot di luar inventory")

    def check_slot(self) -> bool:
        return self.count_empty_slots() > 0

    def count_empty_slots(self) -> int:
        return sum(item is None for item in self.items)

    def add_item(self, item: Item) -> None:
        if not isinstance(item, Item):
            raise ValueError("Inventory hanya menerima Item")
        if any(entry is item for entry in self.items):
            raise ValueError("Objek item yang sama sudah ada")
        for index, current in enumerate(self.items):
            if current is None:
                self.items[index] = item
                return
        raise ValueError("Inventory penuh")

    def get_item(self, slot: int) -> Item:
        self.validate_slot(slot)
        item = self.items[slot]
        if item is None:
            raise IndexError("Tidak ada item pada slot ini")
        return item

    def remove_item(self, slot: int) -> Item:
        item = self.get_item(slot)
        self.items[slot] = None
        return item

    def move_item(self, from_slot: int, to_slot: int) -> None:
        self.validate_slot(from_slot)
        self.validate_slot(to_slot)
        self.items[from_slot], self.items[to_slot] = self.items[to_slot], self.items[from_slot]

    def __len__(self) -> int:
        return self.max_item - self.count_empty_slots()
