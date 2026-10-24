import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from cli.console import describe_options
from content.catalog import create_player, create_goblin, create_stock
from content.short_stories import create_short_story
from core.game_session import GameSession
from core.models import Choice, ConditionalChoice
from events.event import Event
from events.monster_event import MonsterEvent
from events.tavern_event import TavernEvent
from events.merchant_event import MerchantEvent

class PosttestTests(unittest.TestCase):
    def test_abstract_class_and_incomplete_subclass_cannot_be_created(self):
        with self.assertRaises(TypeError):
            Event("id", "title", "description")
        class IncompleteEvent(Event):
            def get_choices(self, session):
                return []
        with self.assertRaises(TypeError):
            IncompleteEvent("id", "title", "description")
        self.assertEqual(Event.__abstractmethods__, {"get_choices", "resolve"})

    def test_subclasses_implement_both_methods_and_share_validation(self):
        session = GameSession(create_player())
        session.player.lose_life()
        events = [MonsterEvent("demo", create_goblin()), TavernEvent(),
                  MerchantEvent(create_stock()), create_short_story()]
        requests = []
        for event in events:
            self.assertFalse(type(event).__abstractmethods__)
            self.assertIs(type(event).validate_choice, Event.validate_choice)
            choice = next(option for option in event.get_choices(session) if option.enabled)
            result = event.resolve(session, choice.choice_id)
            requests.append((result.battle_request is not None, result.completed))
            with self.assertRaises(ValueError):
                event.validate_choice(session, "invalid")
        self.assertIn((True, False), requests)
        self.assertIn((False, True), requests)

    def test_unrelated_choices_use_one_duck_typed_function(self):
        self.assertFalse(issubclass(Choice, ConditionalChoice))
        self.assertFalse(issubclass(ConditionalChoice, Choice))
        normal = Choice("a", "Aksi")
        checked = ConditionalChoice("b", "Cek", "charisma", 18)
        self.assertEqual(describe_options([normal, checked]), ["Aksi", "Cek [CHARISMA, kesulitan 18]"])

if __name__ == "__main__":
    unittest.main()
