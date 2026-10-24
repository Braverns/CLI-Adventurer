from core.enums import EquipmentSlot
from items.equippable_item import EquippableItem


class Equipment:
    def __init__(self) -> None:
        self.head = None
        self.chest = None
        self.back = None
        self.legs = None
        self.boots = None
        self.main_hand = None
        self.off_hand = None

    def get_equipped(self, slot: EquipmentSlot):
        if not isinstance(slot, EquipmentSlot):
            raise ValueError("Slot equipment tidak valid")

        return getattr(self, slot.value)

    def get_candidate_slots(self, item) -> list:
        candidates = []

        for slot in EquipmentSlot:
            if slot in item.allowed_slots:
                candidates.append(slot)

        return candidates

    def equip_from_inventory(self, player, inventory_slot: int, target_slot = None) -> None:
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

            empty = []
            has_blocked_slot = False

            for slot in candidates:
                if slot in blocked:
                    has_blocked_slot = True

                if self.get_equipped(slot) is None and slot not in blocked:
                    empty.append(slot)

            if not empty and has_blocked_slot:
                raise ValueError("Slot diblokir senjata dua tangan; pilih slot penggantian secara eksplisit")

            if not empty and len(candidates) > 1:
                raise ValueError("Kedua tangan terisi; pilih slot yang ingin diganti")

            if empty:
                target_slot = empty[0]
            else:
                target_slot = candidates[0]

        if not item.can_use_slot(target_slot):
            raise ValueError("Item tidak cocok dengan slot tersebut")

        conflicts = {target_slot}

        conflicts.update(item.occupied_slots)

        for slot in EquipmentSlot:
            equipped = self.get_equipped(slot)

            if equipped is not None and target_slot in equipped.occupied_slots:
                conflicts.add(slot)

        removed = []

        for slot in EquipmentSlot:
            equipped = self.get_equipped(slot)

            if slot in conflicts and equipped is not None:
                removed.append(equipped)

        planned_inventory = player.inventory.items.copy()
        planned_inventory[inventory_slot] = None
        empty_slots = 0

        for entry in planned_inventory:
            if entry is None:
                empty_slots += 1

        if empty_slots < len(removed):
            raise ValueError("Inventory tidak cukup untuk equipment yang dilepas")

        for old_item in removed:
            empty_index = planned_inventory.index(None)
            planned_inventory[empty_index] = old_item

        removed_traits = []

        for old_item in removed:
            for trait_entry in old_item.traits:
                removed_traits.append(trait_entry)

        self._change_traits(player, removed_traits, item.traits)

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

        self._change_traits(player, item.traits, [])
        player.inventory.add_item(item)
        setattr(self, slot.value, None)

    def _change_traits(self, player, removed: list, added: list) -> None:
        changes = {}
        examples = {}

        for entry in removed:
            trait_type = type(entry.trait)

            if trait_type not in changes:
                changes[trait_type] = 0

            changes[trait_type] -= entry.stack
            examples[trait_type] = entry.trait

        for entry in added:
            trait_type = type(entry.trait)

            if trait_type not in changes:
                changes[trait_type] = 0

            changes[trait_type] += entry.stack
            examples[trait_type] = entry.trait

        for trait_type, amount in changes.items():
            current_stack = 0
            trait = examples[trait_type]

            if trait_type in player.trait_manager.traits:
                current_entry = player.trait_manager.traits[trait_type]
                current_stack = current_entry.stack
                trait = current_entry.trait

            new_stack = current_stack + amount

            if new_stack < 0 or new_stack > trait.max_stack:
                raise ValueError(f"Stack {trait.name} di luar batas")

        for trait_type, amount in changes.items():
            trait = examples[trait_type]

            if amount < 0:
                player.trait_manager.remove_trait(trait, player, -amount)

            if amount > 0:
                player.trait_manager.add_trait(trait, player, amount)
