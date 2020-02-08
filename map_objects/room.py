class Room:
    """Room class. Defines a room given position and dimensions
    """

    def __init__(self, x: int, y: int, w: int, h: int):
        """Rom initializer
        
        Arguments:
            x {int} -- x origin
            y {int} -- y origin
            w {int} -- width of the room
            h {int} -- height of the room
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

