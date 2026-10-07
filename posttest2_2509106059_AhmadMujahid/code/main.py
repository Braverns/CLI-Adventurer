from characters.monster import Monster
from characters.player import Player
from characters.combatant import Combatant
from characters.classes.profession import Profession
from utils.stats import Stats
from utils.traits.resource_trait import LuckiestAdventurer
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong
from combat.battle import Battle
from inventory.inventory import Inventory
from items.weapon import CorosionDagger, VenomousAxe
from items.armor import CorosionSpikeArmor, GiantArmor
from items.item import Item


def show_inventory(player: Player) -> None:
    for index, item in enumerate(player.inventory.items):
        if item is not None:
            print(f"Slot {index}: {item.name}")


def show_traits(player: Player) -> None:
    if not player.trait_manager.traits:
        print("Tidak ada trait aktif")
        return

    for entry in player.trait_manager.traits.values():
        print(f"- {entry.trait.name}: {entry.stack} stack")


def main() -> None:

    #  __________________________________________
    # | 1. MEMBUAT PLAYER DAN MONSTER            |
    # |__________________________________________|
    bravern = Player(name="Bravern", stats=Stats(10, 8, 5, 3, 1), lives=10, level=1, gold=100, 
                     profession=Profession("Warrior", Stats(5, 3, 3, 0, 0)))
    goblin = Monster(name="Goblin", stats=Stats(5, 5, 2, 3, 0), rarity="Common", monster_type="Physical")

    print(bravern.get_info())
    print(goblin.get_info())
    print(f"Strength Bravern setelah bonus profession: {bravern.stats.strength}\n")

    assert bravern.stats.strength == 15


    #  __________________________________________
    # | 2. TEST TRAIT STATS DAN RESOURCE         |
    # |__________________________________________|
    strong = Strong()
    lucky = LuckiestAdventurer()

    bravern.trait_manager.add_trait(strong, bravern, 2)

    print(f"Strong x2 -> Strength: {bravern.stats.strength}")

    assert bravern.stats.strength == 25

    bravern.trait_manager.remove_trait(strong, bravern, 2)

    print(f"Strong dilepas -> Strength: {bravern.stats.strength}")

    assert bravern.stats.strength == 15

    bravern.trait_manager.add_trait(lucky, bravern, 2)

    bravern.trait_manager.trigger_reward(bravern)

    print(f"Luckiest Adventurer x2 -> Gold: {bravern.gold}\n")

    assert bravern.gold == 120

    bravern.trait_manager.remove_trait(lucky, bravern, 2)


    #  __________________________________________
    # | 3. TEST INVENTORY                        |
    # |__________________________________________|
    dagger = CorosionDagger()
    axe = VenomousAxe()
    spike_armor = CorosionSpikeArmor()
    giant_armor = GiantArmor()

    bravern.inventory.add_item(dagger)
    bravern.inventory.add_item(axe)
    bravern.inventory.add_item(spike_armor)
    bravern.inventory.add_item(giant_armor)

    print("Isi inventory awal:")
    show_inventory(bravern)

    bravern.inventory.move_item(3, 4)

    assert (bravern.inventory.get_item(4) is giant_armor)

    bravern.inventory.move_item(4, 3)

    print("Move item berhasil\n")


    #  __________________________________________
    # | 4. TEST EQUIPMENT DAN TRAIT DARI ITEM    |
    # |__________________________________________|
    bravern.equip_from_inventory(0)

    print(f"Weapon: {bravern.equipment.weapon.name}") # type: ignore
    show_traits(bravern)

    bravern.equip_from_inventory(1)

    print(f"\nWeapon diganti menjadi: {bravern.equipment.weapon.name}") # type: ignore
    show_traits(bravern)

    bravern.equip_from_inventory(2)

    print(f"\nArmor: {bravern.equipment.armor.name}") # type: ignore
    show_traits(bravern)

    bravern.equip_from_inventory(3)

    print(f"\nArmor diganti menjadi: {bravern.equipment.armor.name}") # type: ignore
    show_traits(bravern)

    assert isinstance(bravern.equipment.weapon, VenomousAxe)
    assert isinstance(bravern.equipment.armor, GiantArmor)
    assert (bravern.trait_manager.traits[Toxin].stack == 1)
    assert (bravern.trait_manager.traits[Strong].stack == 3)
    assert bravern.stats.strength == 30

    print("\nIsi inventory setelah replacement:")

    show_inventory(bravern)


    #  __________________________________________
    # | 5. TEST ITEM YANG TIDAK BISA DI-EQUIP    |
    # |__________________________________________|
    potion = Item("Potion")

    bravern.inventory.add_item(potion)

    potion_slot = (bravern.inventory.items.index(potion))

    try:
        bravern.equip_from_inventory(potion_slot)

    except ValueError as error:
        print(f"Error berhasil ditangkap: {error}")

    assert potion in bravern.inventory.items

    print("Potion tetap berada di inventory\n")


    #  __________________________________________
    # | 6. TEST INVENTORY PENUH                  |
    # |__________________________________________|
    full_inventory = Inventory()

    for number in range(full_inventory.max_item):
        full_inventory.add_item(Item(f"Item {number + 1}"))

    try:
        full_inventory.add_item(Item("Extra Item"))

    except ValueError as error:
        print(f"Error inventory penuh berhasil ditangkap: {error}\n")

    assert not full_inventory.check_slot()


    #  __________________________________________
    # | 7. TEST BATTLE DAN STATUS TOXIN          |
    # |__________________________________________|
    toxin_entry = (bravern.trait_manager.traits[Toxin])

    # Dibuat 100% hanya untuk testing.
    toxin_entry.trait.chance = 1.0 # type: ignore

    bravern_combatant = Combatant(owner=bravern, max_health=100)
    goblin_combatant = Combatant(owner=goblin, max_health=100)

    battle = Battle(bravern_combatant, goblin_combatant)

    winner = battle.start()

    print(f"\nPemenang battle: {winner.owner.name}")

    assert winner.owner is bravern
    assert not goblin_combatant.is_alive()


    #  __________________________________________
    # | 8. HASIL AKHIR TEST                      |
    # |__________________________________________|
    print(" _______________________________________")
    print("|                                       |")
    print("| Semua test utama berhasil dijalankan. |")
    print("|_______________________________________|")


if __name__ == "__main__":
    main()