from characters.player import Player
from characters.monster import Monster

class Battle:
    def __init__(self, player: Player, enemy: Monster):
        self.player = player
        self.enemy = enemy

    def determine_first_turn(self) -> Player | Monster:
        if self.player.stats.agility >= self.enemy.stats.agility:
            return self.player
        else:
            return self.enemy 

    def start(self) -> Player | Monster:
        attacker = self.determine_first_turn()

        if attacker == self.player:
            target = self.enemy
        else:
            target = self.player

        while True:
            attacker.attack(target)
            print(f'{attacker.name} menyerang {target.name} sebesar {attacker.stats.strength} damage!')
            print(f'darah {target.name} tersisa {target.health}\n')

            if not target.is_alive():
                print(f'{attacker.name} telah menang!')
                return attacker

            attacker, target = target, attacker


