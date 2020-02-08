from map_objects.tile import Tile
from map_objects.room import Room


class GameMap:
    """GameMap class. instantiate a GameMap with a tile grid
    """

    def __init__(self, width: int, height: int):
        """GameMap initializer
        
        Arguments:
            width {int} -- map width
            height {int} -- map height
        """
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self) -> list:
        """Initialize the tile map
        
        Returns:
            list -- tile grid
        """
        # Initialize the WxH tile grid with non-blocking tiles
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self):
        # Define room objects
        room1 = Room(x=20, y=15, w=10, h=15)
        room2 = Room(x=35, y=15, w=10, h=15)

        self.create_room(room1)
        self.create_room(room2)

    def create_room(self, room: Room):
        """Carve out a room in the GameMap
        
        Arguments:
            room {Room} -- room object containing dimensions for the room
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def is_blocked(self, x: int, y: int) -> bool:
        """Checks if given map position is blocked
        
        Arguments:
            x {int} -- x position
            y {int} -- y position
        
        Returns:
            bool -- Blocking state of target tile
        """
        return self.tiles[x][y].blocked
