import sys
from pathlib import Path
import unittest
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from characters.combatant import Combatant
from combat.battle import Battle
from content.catalog import create_player, create_goblin
from core.game_session import GameSession
from utils.traits.battle_trait import PoisonStatus

class BattleTests(unittest.TestCase):
    def test_hp_clamp_and_negative_damage(self):
        unit = Combatant(create_player(), 100)
        unit.health = 150
        self.assertEqual(unit.health, 100)
        unit.take_damage(200)
        self.assertEqual(unit.health, 0)
        with self.assertRaises(ValueError):
            unit.take_damage(-1)

    def test_status_death_before_attack_and_idempotent_result(self):
        player = Combatant(create_player(), 100)
        enemy = Combatant(create_goblin(), 100)
        player.add_status(PoisonStatus(3, 9, 1.0))
        battle = Battle(player, enemy, Random(1))
        battle.step()
        self.assertIs(battle.get_result().winner, enemy)
        self.assertEqual(enemy.health, 100)
        self.assertEqual(battle.step(), [])

    def test_status_duration_refresh_is_capped(self):
        unit = Combatant(create_player(), 100)
        unit.add_status(PoisonStatus(3, 9, 0.03))
        unit.add_status(PoisonStatus(8, 9, 0.03))
        self.assertEqual(len(unit.statuses), 1)
        self.assertEqual(unit.statuses[0].duration, 9)

    def test_equal_agility_prioritizes_player_and_damage_has_floor(self):
        player = Combatant(create_player(), 100)
        enemy = Combatant(create_goblin(), 100)
        enemy.owner.stats.agility = player.owner.stats.agility
        enemy.owner.stats.defense = 999
        battle = Battle(player, enemy)
        self.assertIs(battle.attacker, player)
        battle.step()
        self.assertEqual(enemy.health, 99)

    def test_completed_battle_is_processed_once_and_next_starts_full(self):
        from test_game_routes import start_at_goblin, resolve_battle
        session = start_at_goblin()
        session.choose("cha")
        old_player_combatant = session.active_battle.player
        old_player_combatant.health = 10
        resolve_battle(session)
        gold = session.player.gold
        self.assertEqual(session.step_battle(), [])
        self.assertEqual(session.player.gold, gold)
        session.choose("fight")
        self.assertEqual(session.active_battle.player.health, 100)
        self.assertIsNot(session.active_battle.player, old_player_combatant)
        self.assertEqual(session.active_battle.player.statuses, [])

    def test_seeded_sessions_have_same_battle_outcome(self):
        for seed in range(8):
            a = GameSession(create_player(), Random(seed))
            b = GameSession(create_player(), Random(seed))
            a.start()
            b.start()
            self.assertEqual(a.active_event.event_id, b.active_event.event_id)

if __name__ == "__main__":
    unittest.main()
