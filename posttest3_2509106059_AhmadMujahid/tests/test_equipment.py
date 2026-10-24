import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from content.catalog import create_player
from core.enums import EquipmentSlot
from items.item import Item
from items.weapon import Weapon, GreatSword
from items.shield import Shield
from utils.traits.stats_trait import Strong
from utils.traits.trait_entry import TraitEntry


class EquipmentTests(unittest.TestCase):
    def setUp(self):
        self.player = create_player()

        self.player.equipment.unequip_to_inventory(self.player, EquipmentSlot.MAIN_HAND)
        self.player.inventory.remove_item(0)

    def equip(self, item, slot = None):
        self.player.inventory.add_item(item)

        index = self.player.inventory.items.index(item)

        self.player.equip_from_inventory(index, slot)

    def test_main_hand_priority_and_choice_when_both_full(self):
        first, second, third = Weapon("A"), Weapon("B"), Weapon("C")

        self.equip(first)
        self.equip(second)
        self.assertIs(self.player.equipment.main_hand, first)
        self.assertIs(self.player.equipment.off_hand, second)

        with self.assertRaises(ValueError):
            self.equip(third)

        self.player.equip_from_inventory(0, EquipmentSlot.OFF_HAND)
        self.assertIs(self.player.equipment.off_hand, third)

    def test_two_handed_counts_released_source_slot(self):
        self.equip(Weapon("Sword"))
        self.equip(Shield())

        for _ in range(8):
            self.player.inventory.add_item(Item("Filler"))

        sword = GreatSword()

        self.player.inventory.add_item(sword)
        self.player.equip_from_inventory(8)
        self.assertIs(self.player.equipment.main_hand, sword)
        self.assertIsNone(self.player.equipment.off_hand)
        self.assertEqual(len(self.player.inventory), 10)

    def test_capacity_failure_keeps_everything(self):
        self.equip(Weapon("Sword"))
        self.equip(Shield())

        for _ in range(9):
            self.player.inventory.add_item(Item("Filler"))

        sword = GreatSword()

        self.player.inventory.add_item(sword)

        before = self.player.inventory.items.copy()
        strength = self.player.stats.strength
        old = self.player.equipment.main_hand

        with self.assertRaises(ValueError):
            self.player.equip_from_inventory(9)

        self.assertEqual(self.player.inventory.items, before)
        self.assertIs(self.player.equipment.main_hand, old)
        self.assertEqual(self.player.stats.strength, strength)

    def test_trait_overflow_does_not_remove_old_equipment(self):
        self.equip(Weapon("Old", traits = [TraitEntry(Strong(), 2)]))
        self.player.trait_manager.add_trait(Strong(), self.player, 18)

        new = Weapon("New", traits = [TraitEntry(Strong(), 3)])

        self.player.inventory.add_item(new)

        strength = self.player.stats.strength

        with self.assertRaises(ValueError):
            self.player.equip_from_inventory(0, EquipmentSlot.MAIN_HAND)

        self.assertEqual(self.player.stats.strength, strength)
        self.assertEqual(self.player.trait_manager.traits[Strong].stack, 20)
        self.assertEqual(self.player.equipment.main_hand.name, "Old")
        self.assertIs(self.player.inventory.get_item(0), new)

    def test_two_handed_is_removed_when_equipping_off_hand(self):
        self.equip(GreatSword())
        self.player.inventory.add_item(Shield())

        with self.assertRaises(ValueError):
            self.player.equip_from_inventory(0)

        self.player.inventory.remove_item(0)
        self.equip(Shield(), EquipmentSlot.OFF_HAND)
        self.assertIsNone(self.player.equipment.main_hand)
        self.assertIsNotNone(self.player.equipment.off_hand)
        self.assertNotIn(Strong, self.player.trait_manager.traits)

    def test_invalid_inventory_index_and_item_do_not_mutate(self):
        self.player.inventory.add_item(Item("Apple"))

        for index in (-1, True, 100):
            with self.assertRaises((ValueError, IndexError)):
                self.player.inventory.remove_item(index)

        with self.assertRaises(ValueError):
            self.player.equip_from_inventory(0)

        self.assertEqual(self.player.inventory.get_item(0).name, "Apple")

if __name__ == "__main__":
    unittest.main()
