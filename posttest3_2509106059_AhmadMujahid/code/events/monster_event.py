from core.models import Choice, EventResult
from events.event import Event


class MonsterEvent(Event):
    def __init__(self, event_id: str, monster) -> None:
        super().__init__(event_id, "Pertemuan Monster", f"{monster.name} menghalangi perjalananmu.")

        self.monster = monster
        self._battle_started = False

    def get_choices(self, session) -> list:
        if self._battle_started:
            return []

        return [Choice("fight", f"Hadapi {self.monster.name}")]

    def resolve(self, session, choice_id: str, payload = None) -> EventResult:
        self.validate_choice(session, choice_id)

        self._battle_started = True

        return EventResult(battle_request = self.monster)

    def on_battle_finished(self, session, result) -> EventResult:
        won = result.winner.owner is session.player

        if won:
            text = 'Jalan kembali terbuka.'
        else:
            text = 'Kamu lolos; perjalanan tetap berlanjut.'

        return EventResult([text], completed = True, outcome_id = "done")
