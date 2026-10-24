from __future__ import annotations

from content.balance import STAT_NAMES, require_integer

class Stats:
    def __init__(self, strength: int, agility: int, defense: int, intelligence: int, charisma: int) -> None:
        for name, value in zip(STAT_NAMES, (strength, agility, defense, intelligence, charisma)):
            require_integer(value, name)
            setattr(self, name, value)

    def add(self, bonus) -> None:
        for name in STAT_NAMES:
            setattr(self, name, getattr(self, name) + getattr(bonus, name))

    def __str__(self) -> str:
        return " | ".join(f"{name}: {getattr(self, name)}" for name in STAT_NAMES)
