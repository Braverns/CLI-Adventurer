from __future__ import annotations

from content.catalog import create_stock, create_travel_monster
from content.short_stories import create_short_story
from core.enums import FlowPhase
from events.merchant_event import MerchantEvent
from events.monster_event import MonsterEvent
from events.tavern_event import TavernEvent

class EventDirector:
    def __init__(self) -> None:
        self.phase = FlowPhase.OPENING_ONE
        self.completed_event_count = 0
        self.travel_events_completed = 0
        self.day = 0
        self.time_phase = "sebelum quest"

    def create_next_event(self, session):
        builders = {
            FlowPhase.OPENING_ONE: self._opening_one,
            FlowPhase.OPENING_TWO: lambda s: s.rng.choice([
                lambda: MerchantEvent(create_stock()), TavernEvent])(),
            FlowPhase.GOBLIN_STORY: self._goblin,
            FlowPhase.TRAVEL: self._travel,
            FlowPhase.ORACHULM_STORY: self._orachulm,
            FlowPhase.REPORT: lambda s: s.quest.create_report_event(),
        }
        return builders[self.phase](session)

    def _opening_one(self, session):
        return session.rng.choice([
            lambda: MonsterEvent("opening_monster", create_travel_monster(session.rng)),
            create_short_story])()

    def _goblin(self, session):
        self.day, self.time_phase = 1, "malam"
        return session.quest.create_goblin_event()

    def _travel(self, session):
        self.day, self.time_phase = 2, "siang"
        return MonsterEvent(f"travel_{self.travel_events_completed + 1}",
                            create_travel_monster(session.rng))

    def _orachulm(self, session):
        self.day, self.time_phase = 2, "malam"
        return session.quest.create_orachulm_event()

    def record_event_completion(self, result) -> None:
        self.completed_event_count += 1
        transitions = {
            FlowPhase.OPENING_ONE: lambda: FlowPhase.OPENING_TWO,
            FlowPhase.OPENING_TWO: lambda: FlowPhase.GOBLIN_STORY,
            FlowPhase.GOBLIN_STORY: lambda: {
                "informed": FlowPhase.TRAVEL, "uninformed": FlowPhase.REPORT,
                "failed": FlowPhase.FINISHED}[result.outcome_id],
            FlowPhase.TRAVEL: self._after_travel,
            FlowPhase.ORACHULM_STORY: lambda: FlowPhase.REPORT,
            FlowPhase.REPORT: lambda: FlowPhase.FINISHED,
        }
        self.phase = transitions[self.phase]()

    def _after_travel(self):
        self.travel_events_completed += 1
        if self.travel_events_completed >= 2:
            return FlowPhase.ORACHULM_STORY
        return FlowPhase.TRAVEL
