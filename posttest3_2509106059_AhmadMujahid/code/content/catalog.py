from __future__ import annotations

from characters.classes.profession import Profession
from characters.monster import Monster
from characters.player import Player
from content.balance import INITIAL_GOLD, INITIAL_LIVES
from items.accessory import Accessory
from items.armor import CorosionSpikeArmor, GiantArmor
from items.shield import Shield
from items.weapon import CorosionDagger, VenomousAxe
from utils.stats import Stats

def create_player(name: str = "Bravern") -> Player:
    name = name.strip()
    if not name:
        raise ValueError("Nama tidak boleh kosong")
    player = Player(name, Stats(10, 8, 5, 3, 3), INITIAL_LIVES, 1, INITIAL_GOLD,
                    Profession("Warrior", Stats(5, 3, 3, 0, 0)))
    player.inventory.add_item(CorosionDagger())
    player.equip_from_inventory(0)
    return player

def create_goblin() -> Monster:
    return Monster("Goblin Pencuri Apel", Stats(9, 6, 3, 2, 1), exp_reward=15, max_health=60)

def create_orachulm() -> Monster:
    return Monster("Orachulm", Stats(23, 7, 8, 3, 3), rarity="Rare",
                   exp_reward=30, gold_reward=35, max_health=120)

def create_wolf() -> Monster:
    return Monster("Serigala Lembah", Stats(12, 10, 3, 1, 0), max_health=65)

def create_boar() -> Monster:
    return Monster("Babi Hutan", Stats(14, 5, 5, 1, 0), max_health=75)

def create_travel_monster(rng) -> Monster:
    return rng.choice([create_wolf, create_boar])()

def create_stock() -> list:
    return [CorosionDagger(), VenomousAxe(), GiantArmor(), CorosionSpikeArmor(), Shield(), Accessory()]
