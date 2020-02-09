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

    def take_damage(self, amount: int):
        """Harming behaviour
        
        Arguments:
            amount {int} -- amount of damage taken
        """
        self.hp -= amount

    def attack(self, target:object):
        """Attacking behaviour
        
        Arguments:
            target {object} -- target entity to receive damage
        """        
        damage = self.atk_power - target.fighter.defense # simple damage calculation

        if damage > 0:
            target.fighter.take_damage(damage)
            print(f"{self.owner.name} attacks {target.name} for {damage} hit points.")
        else:
            print(
                f"{self.owner.name.capitalize()} attacks {target.name} but does no damage."
            )
