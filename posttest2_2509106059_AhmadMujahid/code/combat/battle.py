from characters.combatant import Combatant

class Battle:
    def __init__(self, player: Combatant, enemy: Combatant) -> None:
        self.player = player
        self.enemy = enemy

    def determine_first_turn(self) -> Combatant:
        if self.player.owner.stats.agility >= self.enemy.owner.stats.agility:
            return self.player
        else:
            return self.enemy 

    def start(self) -> Combatant:
        attacker = self.determine_first_turn()

        if attacker == self.player:
            target = self.enemy
        else:
            target = self.player

        while True:
            attacker.process_statuses()
            if not attacker.is_alive():
                print(f'{target.owner.name} telah menang!')
                return target
            
            attacker.attack(target)
            print(f'{attacker.owner.name} menyerang {target.owner.name} sebesar {attacker.owner.stats.strength} damage!')
            print(f'darah {target.owner.name} tersisa {target.health}\n')

            if not target.is_alive():
                print(f'{attacker.owner.name} telah menang!')
                return attacker

            attacker.owner.trait_manager.trigger_attack(attacker, target)
            attacker, target = target, attacker


