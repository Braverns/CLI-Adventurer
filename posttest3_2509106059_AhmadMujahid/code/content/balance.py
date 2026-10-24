STAT_POINTS_PER_LEVEL = 5
INITIAL_LIVES = 3
INITIAL_GOLD = 100
COMBAT_MAX_HEALTH = 100
TAVERN_COST = 25
QUEST_GOLD = 40
QUEST_EXP = 10
INTERROGATION_DIFFICULTY = 18
STAT_NAMES = ("strength", "agility", "defense", "intelligence", "charisma")


def require_integer(value: int, label: str, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} harus bilangan bulat minimal {minimum}")


def exp_to_next_level(level: int) -> int:
    return 20 * level


def calculate_damage(attacker, target) -> int:
    return max(1, attacker.stats.strength - target.stats.defense)


def check_success(stat_value: int, difficulty: int, rng) -> bool:
    return rng.randint(1, 20) + stat_value >= difficulty


def sell_price(item) -> int:
    return item.price // 2
