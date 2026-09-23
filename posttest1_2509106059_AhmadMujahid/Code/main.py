from characters.player import Player
from characters.monster import Monster
from characters.classes.profession import Profession
from utils.stats import Stats
from utils.trait import Strong
from item.item import Equipment, Weapon
from combat.battle import Battle


def main() -> None:

    # CLASS METHOD
    warrior = Profession("Warrior", Stats(5, 2, 3, 0, 0))
    mage = Profession("Mage", Stats(0, 2, 0, 5, 3))
    default_profession = Profession.create_default("Adventurer")

    print(" __________________ ")
    print("|   CLASS METHOD   |")
    print(default_profession.name)
    print()




    print(" ___________________ ")
    print("|   STATIC METHOD   |")
    print(Stats.is_valid_stat(10))
    print(Stats.is_valid_stat(-5))
    print()


    # PLAYER
    bravern = Player(name = "Bravern", level = 1, health = 25.5, profession = warrior, stats = Stats(10, 10, 10, 10, 10))
    arthur = Player(name = "Arthur", level = 2, health = 30, profession = mage , stats = Stats(8, 8, 8, 12, 10))


    # MONSTER
    goblin = Monster(name = "Goblin", rarity = "Common", monster_type = "Physical", health = 20, stats = Stats(5, 5, 1, 3, 0))
    ogre = Monster(name = "Ogre", rarity = "Uncommon", monster_type = "Physical", health = 100, stats = Stats(20, 3, 10, 2, 1))


    # GETTER
    print(" ____________")
    print("|   GETTER   |")
    print(f"Health Bravern: {bravern.health}")
    print()


    # SETTER VALID
    print(" __________________ ")
    print("|   SETTER VALID   |")
    bravern.health = 30
    print(f"Health setelah valid: {bravern.health}")
    print()


    # SETTER INVALID
    print(" ____________________ ")
    print("|   SETTER INVALID   |")
    bravern.health = -10
    print(f"Health setelah input -10: {bravern.health}")
    print()


    # EQUIPMENT + STRONG
    print(" ________________________ ")
    print("|   EQUIPMENT + STRONG   |")
    sword = Weapon("Iron Sword", Strong())
    equipment = Equipment()
    print(f"Strength sebelum equip: {bravern.stats.strength}")
    equipment.equip_weapon(sword, bravern)
    print(f"Strength setelah equip: {bravern.stats.strength}")
    equipment.unequip_weapon(bravern)
    print(f"Strength setelah unequip: {bravern.stats.strength}")
    print()



    # INSTANCE METHOD
    print(" _____________________ ")
    print("|   INSTANCE METHOD   |")
    print(f"Bravern alive: {bravern.is_alive()}")
    bravern.take_damage(5)
    print(f"Health Bravern: {bravern.health}")
    print(f"Bravern alive: {bravern.is_alive()}")
    print()


    
    # BATTLE
    print(" ____________ ")
    print("|   BATTLE   |")
    battle = Battle(bravern, goblin)
    battle.start()

main()
