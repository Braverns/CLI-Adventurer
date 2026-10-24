import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from content.catalog import create_player
from core.game_session import GameSession
from events.merchant_event import MerchantEvent
from events.tavern_event import TavernEvent
from items.item import Item


class EconomyTests(unittest.TestCase):
    def setUp(self):
        self.player = create_player()
        self.session = GameSession(self.player)

    def test_multiple_levels_give_exactly_five_each_and_remainder(self):
        strength = self.player.stats.strength

        self.assertEqual(self.player.gain_experience(65), 2)
        self.assertEqual((self.player.level, self.player.stat_points, self.player.experience), (3, 10, 5))
        self.assertEqual(self.player.stats.strength, strength)
        self.player.allocate_stat_points("intelligence", 5)
        self.assertEqual(self.player.stats.intelligence, 8)
        self.assertEqual(self.player.stat_points, 5)
        self.player.gain_experience(1)
        self.assertEqual(self.player.stat_points, 5)

    def test_invalid_allocation_does_not_consume_points(self):
        self.player.gain_experience(20)

        for name, amount in (("unknown", 1), ("strength", 6), ("strength", 0),
                             ("strength", -1), ("strength", True), ("strength", 1.5)):
            with self.assertRaises(ValueError):
                self.player.allocate_stat_points(name, amount)

        self.assertEqual(self.player.stat_points, 5)

    def test_merchant_buy_sell_and_full_inventory_rejection(self):
        item = Item("Test", 30)
        merchant = MerchantEvent([item])

        merchant.resolve(self.session, "buy:0")
        self.assertEqual(self.player.gold, 70)
        merchant.resolve(self.session, "sell:0")
        self.assertEqual(self.player.gold, 85)
        self.assertEqual(len(self.player.inventory), 0)

        for _ in range(10):
            self.player.inventory.add_item(Item("Full"))

        with self.assertRaises(ValueError):
            merchant.resolve(self.session, "buy:0")

        self.assertEqual(self.player.gold, 85)
        self.assertIs(merchant.stock[0], item)

    def test_unaffordable_purchase_and_empty_sale_do_not_mutate(self):
        merchant = MerchantEvent([Item("Mahal", 500)])

        with self.assertRaises(ValueError):
            merchant.resolve(self.session, "buy:0")

        with self.assertRaises(ValueError):
            merchant.resolve(self.session, "sell:0")

        self.assertEqual(self.player.gold, 100)

    def test_tavern_rest_leave_and_full_lives(self):
        tavern = TavernEvent()

        with self.assertRaises(ValueError):
            tavern.resolve(self.session, "rest")

        self.assertEqual(self.player.gold, 100)
        self.player.lose_life()

        result = tavern.resolve(self.session, "rest")

        self.assertTrue(result.completed)
        self.assertEqual((self.player.lives, self.player.gold), (3, 75))

        before = self.player.gold

        tavern.resolve(self.session, "leave")
        self.assertEqual(self.player.gold, before)

    def test_tavern_insufficient_gold(self):
        self.player.lose_life()
        self.player.spend_gold(100)

        with self.assertRaises(ValueError):
            TavernEvent().resolve(self.session, "rest")

        self.assertEqual((self.player.lives, self.player.gold), (2, 0))

    def test_original_resource_trait_can_update_player_gold(self):
        from utils.traits.resource_trait import LuckiestAdventurer

        lucky = LuckiestAdventurer()

        self.player.trait_manager.add_trait(lucky, self.player, 2)
        self.player.trait_manager.trigger_reward(self.player)

        self.assertEqual(self.player.gold, 120)

if __name__ == "__main__":
    unittest.main()
