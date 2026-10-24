import random
from utils.traits.trait import Trait
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.combatant import Combatant

class BattleTrait(Trait):
    def __init__(self, name: str, description: str, icon: str, max_stack: int, chance: float) -> None:
        super().__init__(name, description, icon, max_stack)
        self.chance = chance

    def on_attack(self, attacker: Combatant, target: Combatant, stack: int) -> None:
        pass
        

class Toxin(BattleTrait):
    def __init__(self) -> None:
        teks: str = "Beracun"
        super().__init__(name = "Toxin", description = teks, icon = "", max_stack = 10, chance = 0.075)
        self.damage_percent = 0.03
        self.duration = 3
        self.max_duration = 9
        

    def on_attack(self, attacker: Combatant, target: Combatant, stack: int) -> None:
        roll = random.random()
        effect = self.get_effect(stack)
        if roll < effect["chance"]:
            status = PoisonStatus(effect["duration"], effect["max_duration"], effect["damage_percent"])
            target.add_status(status)

    def get_effect(self, stack: int) -> dict:
        effect = {"chance": self.chance * stack, "damage_percent": self.damage_percent, 
                   "duration": self.duration, "max_duration": self.max_duration}
        return effect

class PoisonStatus:
    def __init__(self, duration: int, max_duration: int, damage_percent: float) -> None:
        self.duration = duration
        self.max_duration = max_duration
        self.damage_percent = damage_percent

    def on_turn(self, target: Combatant) -> None:
        damage = target.max_health * self.damage_percent
        target.take_damage(damage)
        self.duration -= 1

    def is_active(self) -> bool:
        return self.duration > 0

    def extend_duration(self, amount: int) -> None:
        self.duration = min(self.duration + amount, self.max_duration)

