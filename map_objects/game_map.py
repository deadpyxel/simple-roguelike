from map_objects.tile import Tile


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
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[32][22].blocked = True
        tiles[32][22].block_sight = True

        return tiles
