from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class Choice:
    choice_id: str
    label: str
    enabled: bool = True
    disabled_reason: str = ""

    def describe(self) -> str:
        return self.label

@dataclass
class ConditionalChoice:
    choice_id: str
    label: str
    required_stat: str
    difficulty: int
    enabled: bool = True
    disabled_reason: str = ""

    def describe(self) -> str:
        return f"{self.label} [{self.required_stat.upper()}, kesulitan {self.difficulty}]"

@dataclass
class EventResult:
    messages: list[str] = field(default_factory=list)
    completed: bool = False
    outcome_id: str = ""
    battle_request: Any = None
    granted_items: list = field(default_factory=list)
    ending_id: str = ""

@dataclass(frozen=True)
class BattleResult:
    winner: Any
    loser: Any

@dataclass(frozen=True)
class EndingResult:
    ending_id: str
    title: str
    text: str
    remaining_lives: int
    level: int
    gold: int
    quest_status: str
    reputation: tuple[str, ...]
