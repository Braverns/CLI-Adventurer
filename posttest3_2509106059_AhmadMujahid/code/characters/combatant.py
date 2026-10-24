from __future__ import annotations
from math import isfinite
from characters.character import Character
from content.balance import calculate_damage

class Combatant:
    def __init__(self, owner: Character, max_health: float | int) -> None:
        if not isfinite(max_health) or max_health <= 0:
            raise ValueError("HP maksimum harus positif dan terbatas")
        self.owner = owner
        self.max_health = max_health
        self.health = max_health
        self.statuses = []

    @property
    def health(self) -> float | int:
        return self.__health

    @health.setter
    def health(self, amount: float | int) -> None:
        if not isfinite(amount):
            raise ValueError("HP harus terbatas")
        self.__health = min(max(amount, 0), self.max_health)

    def is_alive(self) -> bool:
        return self.health > 0

    def take_damage(self, damage: float | int) -> None:
        if not isfinite(damage) or damage < 0:
            raise ValueError("Damage tidak valid")
        self.health -= damage

    def attack(self, target: Combatant) -> int:
        damage = calculate_damage(self.owner, target.owner)
        target.take_damage(damage)
        return damage

    def add_status(self, new_status) -> None:
        for status in self.statuses:
            if type(status) is type(new_status):
                status.extend_duration(new_status.duration)
                return
        self.statuses.append(new_status)

    def process_statuses(self) -> list[str]:
        active = []
        logs = []
        for status in self.statuses:
            before = self.health
            status.on_turn(self)
            logs.append(f"{self.owner.name} terkena status: HP berkurang {before - self.health:g}.")
            if status.is_active():
                active.append(status)
        self.statuses = active
        return logs
