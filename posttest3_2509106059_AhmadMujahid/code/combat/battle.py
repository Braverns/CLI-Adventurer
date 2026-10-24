from __future__ import annotations

from random import Random
from characters.combatant import Combatant
from core.models import BattleResult

class Battle:
    def __init__(self, player: Combatant, enemy: Combatant, rng=None) -> None:
        self.player = player
        self.enemy = enemy
        self.rng = rng if rng is not None else Random()
        self.attacker = self.determine_first_turn()
        self.target = enemy if self.attacker is player else player
        self._result = None

    @property
    def finished(self) -> bool:
        return self._result is not None

    def determine_first_turn(self) -> Combatant:
        if self.player.owner.stats.agility >= self.enemy.owner.stats.agility:
            return self.player
        return self.enemy

    def _finish(self, winner, loser) -> list[str]:
        self._result = BattleResult(winner, loser)
        return [f"{winner.owner.name} telah menang!"]

    def step(self) -> list[str]:
        if self.finished:
            return []
        attacker, target = self.attacker, self.target
        logs = attacker.process_statuses()
        if not attacker.is_alive():
            return logs + self._finish(target, attacker)
        damage = attacker.attack(target)
        logs.append(f"{attacker.owner.name} menyerang {target.owner.name}: {damage} damage; "
                    f"HP target {target.health:g}/{target.max_health:g}.")
        if not target.is_alive():
            return logs + self._finish(attacker, target)
        attacker.owner.trait_manager.trigger_attack(attacker, target, self.rng)
        if not target.is_alive():
            return logs + self._finish(attacker, target)
        self.attacker, self.target = target, attacker
        return logs

    def get_result(self) -> BattleResult:
        if self._result is None:
            raise ValueError("Battle belum selesai")
        return self._result

    def start(self) -> BattleResult:
        while not self.finished:
            self.step()
        return self.get_result()
