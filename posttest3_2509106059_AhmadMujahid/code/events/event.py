from __future__ import annotations

from core.models import EventResult

class Event:
    def __init__(self, event_id: str, title: str, description: str) -> None:
        self.event_id = event_id
        self.title = title
        self.description = description
        self._completed = False

    @property
    def completed(self) -> bool:
        return self._completed

    def get_info(self) -> str:
        return f"{self.title}\n{self.description}"

    def validate_choice(self, session, choice_id: str) -> None:
        if self._completed:
            raise ValueError("Event sudah selesai")
        choices = {choice.choice_id: choice for choice in self.get_choices(session)}
        if choice_id not in choices:
            raise ValueError("Pilihan tidak tersedia")
        choice = choices[choice_id]
        if not choice.enabled:
            raise ValueError(choice.disabled_reason or "Pilihan terkunci")

    def get_choices(self, session) -> list:
        raise NotImplementedError

    def resolve(self, session, choice_id: str, payload=None) -> EventResult:
        raise NotImplementedError

    def on_battle_finished(self, session, result) -> EventResult:
        raise ValueError("Event ini tidak sedang menunggu battle")
