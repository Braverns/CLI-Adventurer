from __future__ import annotations

from characters.character import Character
from characters.classes.profession import Profession
from content.balance import STAT_NAMES, STAT_POINTS_PER_LEVEL, exp_to_next_level, require_integer
from equipment.equipment import Equipment
from inventory.inventory import Inventory
from utils.stats import Stats

class Player(Character):
    def __init__(self, name: str, stats: Stats, lives: int, level: int, gold: int,
                 profession: Profession, max_lives: int | None = None) -> None:
        super().__init__(name, stats)
        require_integer(lives, "Nyawa")
        require_integer(level, "Level", 1)
        require_integer(gold, "Gold")
        self.max_lives = lives if max_lives is None else max_lives
        require_integer(self.max_lives, "Nyawa maksimum", 1)
        if lives > self.max_lives:
            raise ValueError("Nyawa melebihi kapasitas")
        self._lives = lives
        self.level = level
        self._experience = 0
        self._stat_points = 0
        self._gold = gold
        self.profession = profession
        self.inventory = Inventory()
        self.equipment = Equipment()
        self.reputation: set[str] = set()
        self.stats.add(profession.stats)

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def gold(self) -> int:
        return self._gold

    @property
    def experience(self) -> int:
        return self._experience

    @property
    def stat_points(self) -> int:
        return self._stat_points

    def lose_life(self) -> None:
        self._lives = max(0, self._lives - 1)

    def recover_life(self) -> None:
        if self._lives >= self.max_lives:
            raise ValueError("Nyawa sudah penuh")
        self._lives += 1

    def spend_gold(self, amount: int) -> None:
        require_integer(amount, "Biaya")
        if amount > self._gold:
            raise ValueError("Gold tidak cukup")
        self._gold -= amount

    def gain_gold(self, amount: int) -> None:
        require_integer(amount, "Gold")
        self._gold += amount

    def gain_experience(self, amount: int) -> int:
        require_integer(amount, "EXP")
        self._experience += amount
        levels = 0
        while self._experience >= exp_to_next_level(self.level):
            self._experience -= exp_to_next_level(self.level)
            self.level += 1
            self._stat_points += STAT_POINTS_PER_LEVEL
            levels += 1
        return levels

    def allocate_stat_points(self, stat_name: str, amount: int) -> None:
        require_integer(amount, "Poin stat", 1)
        if stat_name not in STAT_NAMES:
            raise ValueError("Nama stat tidak valid")
        if amount > self._stat_points:
            raise ValueError("Poin stat tidak cukup")
        setattr(self.stats, stat_name, getattr(self.stats, stat_name) + amount)
        self._stat_points -= amount

    def equip_from_inventory(self, slot: int, target_slot=None) -> None:
        self.equipment.equip_from_inventory(self, slot, target_slot)

    def get_info(self) -> str:
        return (f"Player: {self.name} | Level: {self.level} | EXP: {self.experience} | "
                f"Poin: {self.stat_points} | Nyawa: {self.lives}/{self.max_lives} | Gold: {self.gold}")
