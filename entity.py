class Entity:
    """A generic class used to represent player, npcs, enemies
    """

    def __init__(self, x: int, y: int, char: str, color: object):
        """Entity initializer
        
        Arguments:
            x {int} -- initial X position
            y {int} -- initial y position
            char {str} -- Character to represent entity
            color {object} -- Color objet used to color character on screen 
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx: int, dy: int):
        """Move entity by given amount
        
        Arguments:
            dx {int} -- adjustment on X axis
            dy {int} -- adjustment on Y axis
        """
        self.x += dx
        self.y += dy
