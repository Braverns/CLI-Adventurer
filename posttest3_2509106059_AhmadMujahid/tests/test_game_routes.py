import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from content.catalog import create_player
from core.enums import FlowPhase, QuestStatus, RunStatus
from core.game_session import GameSession


class FixedRandom:
    def __init__(self, roll = 20, alternative = 0):
        self.roll = roll
        self.alternative = alternative

    def choice(self, values):
        return values[self.alternative % len(values)]

    def randint(self, low, high):
        return self.roll

    def random(self):
        return 1.0


def resolve_battle(session, win = True):
    battle = session.active_battle

    if win:
        battle.player.owner.stats.strength = 500
        battle.player.owner.stats.agility = 500
        battle.enemy.owner.stats.strength = 1
        battle.enemy.owner.stats.defense = 0
        battle.attacker, battle.target = battle.player, battle.enemy
    else:
        battle.enemy.owner.stats.strength = 500
        battle.player.owner.stats.defense = 0
        battle.attacker, battle.target = battle.enemy, battle.player

    for _ in range(100):
        if session.active_battle is None:
            return

        session.step_battle()

    raise AssertionError("Battle tidak berakhir")


def start_at_goblin(roll = 20, lives = None):
    session = GameSession(create_player(), FixedRandom(roll, alternative = 1))

    session.start()

    if lives is not None:
        while session.player.lives > lives:
            session.player.lose_life()

    session.choose("leave")
    session.choose("leave")
    assert session.director.phase is FlowPhase.GOBLIN_STORY

    return session


def reach_orachulm(session, lose_travel = False):
    session.choose("cha")
    resolve_battle(session)

    for index in range(2):
        session.choose("fight")
        resolve_battle(session, win = not (lose_travel and index == 0))

    assert session.director.phase is FlowPhase.ORACHULM_STORY


class GameRoutesTests(unittest.TestCase):
    def test_short_route_and_repeat_final_action(self):
        session = start_at_goblin()

        session.choose("attack")
        resolve_battle(session)
        self.assertEqual(session.director.travel_events_completed, 0)
        session.choose("report")
        self.assertEqual(session.ending.ending_id, "APPLE_GOBLIN_RESOLVED")

        gold = session.player.gold

        with self.assertRaises(ValueError):
            session.choose("report")

        self.assertEqual(session.player.gold, gold)

    def test_all_interrogation_stats_success_and_failure(self):
        for action in ("cha", "int", "str"):
            for roll, succeeds in ((20, True), (1, False)):
                with self.subTest(action = action, roll = roll):
                    session = start_at_goblin(roll)

                    session.choose(action)
                    self.assertEqual(session.quest.knows_orachulm, succeeds)

                    with self.assertRaises(ValueError):
                        session.choose(action)

                    resolve_battle(session)

                    if succeeds:
                        expected = FlowPhase.TRAVEL
                    else:
                        expected = FlowPhase.REPORT

                    self.assertIs(session.director.phase, expected)

    def test_goblin_defeat_fails_quest(self):
        session = start_at_goblin()

        session.choose("attack")
        resolve_battle(session, win = False)
        self.assertEqual(session.player.lives, 2)
        self.assertIs(session.quest.status, QuestStatus.FAILED)
        self.assertEqual(session.ending.ending_id, "APPLE_FAILED")

    def test_death_before_quest(self):
        session = GameSession(create_player(), FixedRandom())

        session.start()
        session.player.lose_life()
        session.player.lose_life()
        session.choose("fight")
        resolve_battle(session, win = False)
        self.assertEqual(session.ending.ending_id, "DEAD")
        self.assertIs(session.quest.status, QuestStatus.NOT_STARTED)

    def test_death_in_goblin_travel_and_orachulm(self):
        for location in ("goblin", "travel", "orachulm"):
            with self.subTest(location = location):
                session = start_at_goblin(lives = 1)

                session.choose("cha")

                if location == "goblin":
                    resolve_battle(session, win = False)
                else:
                    resolve_battle(session)
                    session.choose("fight")
                    resolve_battle(session, win = location != "travel")

                    if location == "orachulm":
                        session.choose("fight")
                        resolve_battle(session)
                        session.choose("fight")
                        resolve_battle(session, win = False)

                self.assertEqual(session.ending.ending_id, "DEAD")
                self.assertIs(session.status, RunStatus.FINISHED)

    def test_loss_in_travel_counts_and_does_not_fail_quest(self):
        session = start_at_goblin()

        reach_orachulm(session, lose_travel = True)
        self.assertEqual(session.director.travel_events_completed, 2)
        self.assertEqual(session.player.lives, 2)
        self.assertIs(session.quest.status, QuestStatus.ACTIVE)
        self.assertEqual((session.director.day, session.director.time_phase), (2, "malam"))

    def test_orachulm_report_win_and_escape(self):
        for action, win, ending in (
            ("report", True, "APPLE_ORC_REPORTED"),
            ("fight", True, "APPLE_ORC_SLAYER"),
            ("fight", False, "APPLE_ORC_ESCAPED"),
        ):
            with self.subTest(ending = ending):
                session = start_at_goblin()

                reach_orachulm(session)
                session.choose(action)

                if action == "fight":
                    resolve_battle(session, win)

                session.choose("report")
                self.assertEqual(session.ending.ending_id, ending)
                self.assertIs(session.quest.status, QuestStatus.SUCCEEDED)

                if ending == "APPLE_ORC_SLAYER":
                    self.assertIn("Orc Slayer", session.player.reputation)
                    self.assertTrue(any(item and item.name == "Great Sword"
                                        for item in session.player.inventory.items))

    def test_full_inventory_reward_can_be_replaced_or_skipped(self):
        from items.item import Item

        for action in ("skip_reward", "replace_reward:0"):
            session = start_at_goblin()

            reach_orachulm(session)

            while session.player.inventory.check_slot():
                session.player.inventory.add_item(Item("Barang"))

            session.choose("fight")
            resolve_battle(session)
            self.assertTrue(session.has_pending_reward)

            with self.assertRaises(ValueError):
                session.choose("report")

            session.choose(action)
            self.assertFalse(session.has_pending_reward)
            session.choose("report")
            self.assertEqual(session.ending.ending_id, "APPLE_ORC_SLAYER")
            self.assertEqual(len(session.player.inventory), 10)

    def test_opening_alternatives_and_initial_time(self):
        from events.monster_event import MonsterEvent
        from events.story_event import StoryEvent
        from events.merchant_event import MerchantEvent
        from events.tavern_event import TavernEvent

        for alternative, first_type, second_type in ((0, MonsterEvent, MerchantEvent),
                                                     (1, StoryEvent, TavernEvent)):
            session = GameSession(create_player(), FixedRandom(alternative = alternative))

            session.start()
            self.assertIsInstance(session.active_event, first_type)
            self.assertEqual(session.director.day, 0)
            session.choose("fight" if alternative == 0 else "leave")

            if alternative == 0:
                resolve_battle(session)

            self.assertIsInstance(session.active_event, second_type)
            session.choose("leave")
            self.assertEqual(session.director.completed_event_count, 2)
            self.assertEqual((session.director.day, session.director.time_phase), (1, "malam"))

if __name__ == "__main__":
    unittest.main()
