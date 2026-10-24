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
            FlowPhase.OPENING_TWO: self._opening_two,
            FlowPhase.GOBLIN_STORY: self._goblin,
            FlowPhase.TRAVEL: self._travel,
            FlowPhase.ORACHULM_STORY: self._orachulm,
            FlowPhase.REPORT: self._report,
        }

        builder = builders[self.phase]

        return builder(session)

    def _opening_one(self, session):
        builders = [self._opening_monster, self._opening_short_story]
        builder = session.rng.choice(builders)

        return builder(session)

    def _opening_monster(self, session):
        monster = create_travel_monster(session.rng)

        return MonsterEvent("opening_monster", monster)

    def _opening_short_story(self, session):
        return create_short_story()

    def _opening_two(self, session):
        builders = [self._merchant, self._tavern]
        builder = session.rng.choice(builders)

        return builder(session)

    def _merchant(self, session):
        stock = create_stock()

        return MerchantEvent(stock)

    def _tavern(self, session):
        return TavernEvent()

    def _goblin(self, session):
        self.day = 1
        self.time_phase = "malam"

        return session.quest.create_goblin_event()

    def _travel(self, session):
        self.day = 2
        self.time_phase = "siang"

        event_id = f"travel_{self.travel_events_completed + 1}"
        monster = create_travel_monster(session.rng)

        return MonsterEvent(event_id, monster)

    def _orachulm(self, session):
        self.day = 2
        self.time_phase = "malam"

        return session.quest.create_orachulm_event()

    def _report(self, session):
        return session.quest.create_report_event()

    def record_event_completion(self, result) -> None:
        self.completed_event_count += 1

        transitions = {
            FlowPhase.OPENING_ONE: FlowPhase.OPENING_TWO,
            FlowPhase.OPENING_TWO: FlowPhase.GOBLIN_STORY,
            FlowPhase.ORACHULM_STORY: FlowPhase.REPORT,
            FlowPhase.REPORT: FlowPhase.FINISHED,
        }

        if self.phase is FlowPhase.GOBLIN_STORY:
            outcomes = {
                "informed": FlowPhase.TRAVEL,
                "uninformed": FlowPhase.REPORT,
                "failed": FlowPhase.FINISHED,
            }

            self.phase = outcomes[result.outcome_id]

            return

        if self.phase is FlowPhase.TRAVEL:
            self.phase = self._after_travel()

            return

        self.phase = transitions[self.phase]

    def _after_travel(self):
        self.travel_events_completed += 1

        if self.travel_events_completed >= 2:
            return FlowPhase.ORACHULM_STORY

        return FlowPhase.TRAVEL
