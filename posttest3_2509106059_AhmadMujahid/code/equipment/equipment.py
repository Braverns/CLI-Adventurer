from __future__ import annotations

from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem

class Equipment:
    def __init__(self) -> None:
        for slot in EquipmentSlot:
            setattr(self, slot.value, None)

    def get_equipped(self, slot: EquipmentSlot):
        if not isinstance(slot, EquipmentSlot):
            raise ValueError("Slot equipment tidak valid")
        return getattr(self, slot.value)

    def get_candidate_slots(self, item) -> list:
        return [slot for slot in EquipmentSlot if slot in item.allowed_slots]

    def equip_from_inventory(self, player, inventory_slot: int, target_slot=None) -> None:
        item = player.inventory.get_item(inventory_slot)
        if not isinstance(item, EquippableItem):
            raise ValueError("Item ini tidak bisa dipasang")
        candidates = self.get_candidate_slots(item)
        if target_slot is None:
            blocked = set()
            for slot in EquipmentSlot:
                equipped = self.get_equipped(slot)
                if equipped is not None:
                    blocked.update(equipped.occupied_slots - {slot})
            empty = [slot for slot in candidates
                     if self.get_equipped(slot) is None and slot not in blocked]
            if not empty and any(slot in blocked for slot in candidates):
                raise ValueError("Slot diblokir senjata dua tangan; pilih slot penggantian secara eksplisit")
            if not empty and len(candidates) > 1:
                raise ValueError("Kedua tangan terisi; pilih slot yang ingin diganti")
            target_slot = (empty or candidates)[0]
        if not item.can_use_slot(target_slot):
            raise ValueError("Item tidak cocok dengan slot tersebut")
        conflicts = {target_slot} | set(item.occupied_slots)
        for slot in EquipmentSlot:
            equipped = self.get_equipped(slot)
            if equipped is not None and target_slot in equipped.occupied_slots:
                conflicts.add(slot)
        removed = [self.get_equipped(slot) for slot in EquipmentSlot
                   if slot in conflicts and self.get_equipped(slot) is not None]
        planned_inventory = player.inventory.items.copy()
        planned_inventory[inventory_slot] = None
        if sum(entry is None for entry in planned_inventory) < len(removed):
            raise ValueError("Inventory tidak cukup untuk equipment yang dilepas")
        for old in removed:
            planned_inventory[planned_inventory.index(None)] = old
        removed_traits = [entry for old in removed for entry in old.traits]
        player.trait_manager.change_traits(removed_traits, item.traits, player)
        for slot in conflicts:
            setattr(self, slot.value, None)
        setattr(self, target_slot.value, item)
        player.inventory.items[:] = planned_inventory

    def unequip_to_inventory(self, player, slot: EquipmentSlot) -> None:
        item = self.get_equipped(slot)
        if item is None:
            raise ValueError("Slot equipment kosong")
        if not player.inventory.check_slot():
            raise ValueError("Inventory penuh")
        player.trait_manager.change_traits(item.traits, [], player)
        player.inventory.add_item(item)
        setattr(self, slot.value, None)
