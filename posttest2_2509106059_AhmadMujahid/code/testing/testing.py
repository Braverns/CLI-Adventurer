from characters.combatant import Combatant
from characters.player import Player
from characters.monster import Monster
from characters.classes.profession import Profession
from utils.traits.battle_trait import Toxin
from utils.traits.stats_trait import Strong
from utils.traits.resource_trait import LuckiestAdventurer
from utils.stats import Stats
from combat.battle import Battle

player = Player("Bravern", Stats(10, 10, 5, 3, 1), 10, 1, 100, Profession("Warrior", Stats(3, 1, 1, 0, 0)))
monster = Monster("Goblin", Stats(5, 5, 1, 3, 0), "Common", "Physical")

player_combatant = Combatant(player, max_health=1000)
monster_combatant = Combatant(monster, max_health=1000)

lucky = LuckiestAdventurer()

player.trait_manager.add_trait(lucky, player, 3)
player.trait_manager.add_trait(lucky, player, 2)
player.trait_manager.trigger_reward(player)
print(player.gold)

player.trait_manager.remove_trait(lucky, player, 3)
player.trait_manager.trigger_reward(player)
print(player.gold)

player.trait_manager.remove_trait(lucky, player, 2)
print(len(player.trait_manager.traits))




















# def display_inventory(self):
#     for i in range(1, 11):

#         if self.items[i - 1] is not None:
            
#             print(f"{[i]}. \t{self.item[i - 1].name}") # type: ignore
#         else:
#             print(f"{[i]}. \tKosong")

