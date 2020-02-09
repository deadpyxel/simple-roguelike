class Tile:
    """Generic Tile class. 
    A tile may or may not be blocked and may or may not block sight
    """

    def __init__(self, blocked: bool, block_sight: bool = None):
        """Tile initializer.
        
        Arguments:
            blocked {bool} -- blocking status of tile
        
        Keyword Arguments:
            block_sight {bool} -- value determining sight status (default: {None})
        """
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight  # flag if tile blocks sight of other tiles
        self.explored = False  # has the player been in this tile yet
