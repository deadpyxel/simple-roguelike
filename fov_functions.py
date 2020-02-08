import tcod as libtcod


def initialize_fov(game_map: object) -> libtcod.map.Map:
    """Initialize the FoV map to block sight of all objects
    
    Arguments:
        game_map {object} -- GameMap object
    
    Returns:
        libtcod.map.Map -- FoV map
    """    
    fov_map = libtcod.map.Map(game_map.width, game_map.height)

    for y in range(game_map.height):
        for x in range(game_map.width):
            libtcod.map_set_properties(
                fov_map,
                x,
                y,
                not game_map.tiles[x][y].block_sight,
                not game_map.tiles[x][y].blocked,
            )
    return fov_map