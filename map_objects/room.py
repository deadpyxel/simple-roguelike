class Room:
    """Room class. Defines a room given position and dimensions
    """

    def __init__(self, x: int, y: int, w: int, h: int):
        """Room initializer
        
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

    def center(self) -> tuple:
        """Returns center of room as a tuple
        
        Returns:
            tuple -- center of the room
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)

    def intersect(self, other: object) -> bool:
        """Checks for room intersection
        
        Arguments:
            other {object} -- other room object to comparison
        
        Returns:
            bool -- True if the rooms intersect
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
