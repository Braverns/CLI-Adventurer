from utils.stats import Stats
from characters.classes.profession import Profession
from characters.character import Character
from equipment.equipment import Equipment
from inventory.inventory import Inventory
from items.weapon import Weapon
from items.armor import Armor

class Player(Character):
    def __init__(self, name: str, stats: Stats, lives: int, level: int, gold: int, profession: Profession) -> None:
        super().__init__(name, stats)
        self.lives = lives
        self.level = level
        self.gold = gold
        self.profession = profession
        self.inventory = Inventory()
        self.equipment = Equipment()

        self.__apply_profession_stats()

    def __apply_profession_stats(self) -> None:
        self.stats.add(self.profession.stats)

    def equip_from_inventory(self, slot: int) -> None:
        item = self.inventory.get_item(slot)

        if not isinstance(item, (Weapon, Armor)):
            raise ValueError("Item ini tidak bisa dipasang")
        
        item = self.inventory.remove_item(slot)

        if isinstance(item, Weapon):
            if self.equipment.weapon is not None:
                weapon = self.equipment.unequip_weapon(self)
                self.inventory.add_item(weapon)

            self.equipment.equip_weapon(item, self)

        elif isinstance(item, Armor): 
            if self.equipment.armor is not None:
                armor = self.equipment.unequip_armor(self)
                self.inventory.add_item(armor)

            self.equipment.equip_armor(item, self) 

    def get_info(self) -> str:

        return ( f"Player: {self.name} | " f"Level: {self.level} | " f"Gold: {self.gold}")


                
