import tcod as libtcod


def render_all(
    con: libtcod.console.Console, entities: list, screen_width: int, screen_height: int
):
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

