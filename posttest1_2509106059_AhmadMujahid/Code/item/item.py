class Equipment:
    def __init__(self) -> None:
        self.armor: Armor | None = None
        self.weapon: Weapon | None = None

    def equip_weapon(self, weapon: Weapon, player) -> None:
        if isinstance(weapon, Weapon):
            self.weapon = weapon
            player.traits_manager.add_trait(weapon.trait)
            player.traits_manager.apply_trait(weapon.trait, player)

    def unequip_weapon(self, player) -> None:
        if self.weapon is not None:
            trait = self.weapon.trait
            player.traits_manager.remove_trait(trait, player)
            self.weapon = None

    



class Weapon:
    def __init__(self, name: str, trait) -> None:
        self.name = name
        self.trait = trait

class Armor:
    pass