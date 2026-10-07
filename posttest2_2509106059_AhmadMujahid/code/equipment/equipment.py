from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.player import Player
    from items.weapon import Weapon
    from items.armor import Armor

class Equipment:
    def __init__(self) -> None:
        self.armor: Armor | None = None
        self.weapon: Weapon | None = None

    def equip_weapon(self, weapon: Weapon, player: Player) -> None:
        if self.weapon is not None:
            self.unequip_weapon(player)

        self.weapon = weapon
        for trait_entry in weapon.traits:
            player.trait_manager.add_trait(trait_entry.trait, player, trait_entry.stack)

    def unequip_weapon(self, player: Player) -> Weapon:
        if self.weapon is None:
            raise ValueError("Tidak ada senjata yang bisa dilepas")

        if not player.inventory.check_slot():
            raise ValueError("Inventory full tidak melepas senjata")

        for trait_entry in self.weapon.traits:
            player.trait_manager.remove_trait(trait_entry.trait, player, trait_entry.stack)

        weapon = self.weapon
        self.weapon = None

        return weapon

    def equip_armor(self, armor: Armor, player: Player) -> None:
        if self.armor is not None:
            self.unequip_armor(player)

        self.armor = armor
        for trait_entry in armor.traits:
            player.trait_manager.add_trait(trait_entry.trait, player, trait_entry.stack)

    def unequip_armor(self, player: Player) -> Armor:
        if self.armor is None:
            raise ValueError("Tidak ada Armor yang bisa dilepas")

        if not player.inventory.check_slot():
            raise ValueError("Inventory full tidak melepas armor")

        for trait_entry in self.armor.traits:
            player.trait_manager.remove_trait(trait_entry.trait, player, trait_entry.stack)

        armor = self.armor
        self.armor = None

        return armor