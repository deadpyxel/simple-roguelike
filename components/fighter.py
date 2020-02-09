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
