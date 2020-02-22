import tcod as libtcod

from game_messages import Message


class Fighter:
    """Fighter component. defines fighting behaviour
    """

    def __init__(self, hp: int, defense: int, power: int):
        """Fighter initializer.
        
        Arguments:
            hp {int} -- Health points
            defense {int} -- Damage mitigation
            power {int} -- Attack strength
        """
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.atk_power = power

    def take_damage(self, amount: int) -> list:
        """Harming behaviour
        
        Arguments:
            amount {int} -- amount of damage taken
        
        Returns:
            list -- results of damage taken
        """
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({"dead": self.owner})
        return results

    def heal(self, amount: int):
        """Self-healing behaviour

        Heals based on the given amount. 
        Does not allow overhelaing
        
        Arguments:
            amount {int} -- Amount to heal
        """        
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target: object) -> list:
        """Attacking behaviour
        
        Arguments:
            target {object} -- target entity to receive damage
        
        Returns:
            list -- list of results from attack action
        """
        results = []  # resulting log
        damage = self.atk_power - target.fighter.defense  # simple damage calculation

        if damage > 0:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name} attacks {target.name} for {damage} hit points."
                    )
                }
            )
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append(
                {
                    "message": Message(
                        f"{self.owner.name.capitalize()} attacks {target.name} but does no damage."
                    )
                }
            )

        return results
