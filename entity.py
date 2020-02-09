class Entity:
    """A generic class used to represent player, npcs, enemies
    """

    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: object,
        name: str,
        blocks: bool = False,
        fighter: object = None,
        ai: object = None,
    ):
        """Entity initializer
        
        Arguments:
            x {int} -- initial X position
            y {int} -- initial y position
            char {str} -- Character to represent entity
            color {object} -- Color objet used to color character on screen 
            name {str} -- Name of the entity
        Keyword Arguments:
            blocks {bool} -- Block behaviour flag (default: {False})
            fighter {object} -- fighting component (default: {None})
            ai {object} -- AI component (default: {None})
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai

        # If components are present, set this entity as owner
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self

    def move(self, dx: int, dy: int):
        """Move entity by given amount
        
        Arguments:
            dx {int} -- adjustment on X axis
            dy {int} -- adjustment on Y axis
        """
        self.x += dx
        self.y += dy


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
