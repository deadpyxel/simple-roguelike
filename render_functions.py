import tcod as libtcod


def render_all(
    con: libtcod.console.Console,
    entities: list,
    game_map: object,
    screen_width: int,
    screen_height: int,
    colors: dict,
):
    """Wrapper funtion to make libtcod calls rendering all entities
    
    Arguments:
        con {libtcod.console.Console} -- target console
        entities {list} -- lsit of entities to be drawn
        game_map {object} -- GameMap object
        screen_width {int} -- screen width
        screen_height {int} -- screen height
        colors {dict} -- colors to be used for the map
    """
    # Draw all map tiles
    for y in range(game_map.height):
        for x in range(game_map.width):
            wall = game_map.tiles[x][y].block_sight

            if wall:
                libtcod.console_set_char_background(
                    con, x, y, colors.get("dark_wall"), libtcod.BKGND_SET
                )
            else:
                libtcod.console_set_char_background(
                    con, x, y, colors.get("dark_ground"), libtcod.BKGND_SET
                )

    # Draw all entities in the list
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)


def clear_all(con: libtcod.console.Console, entities: list):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con: libtcod.console.Console, entity: object):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con: libtcod.console.Console, entity: object):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)

