from enum import Enum, auto

import tcod as libtcod


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def render_bar(
    panel: libtcod.console.Console,
    x: int,
    y: int,
    total_width: int,
    label: str,
    val: int,
    maximum: int,
    fg_color: libtcod.Color,
    bg_color: libtcod.Color,
):
    """UI Bar rendering function
    
    Arguments:
        panel {libtcod.console.Console} -- Target console to draw the bar
        x {int} -- x position
        y {int} -- y position
        total_width {int} -- total desired width
        label {str} -- label for the bar
        val {int} -- current value for the bar
        maximum {int} -- maximum expected value for the bar
        fg_color {libtcod.Color} -- foreground color
        bg_color {libtcod.Color} -- background color
    """
    bar_width = int(val / maximum * total_width)

    # Render bar
    libtcod.console_set_default_background(panel, bg_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)
    libtcod.console_set_default_background(panel, fg_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # Render text
    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(
        panel,
        int(x + total_width / 2),
        y,
        libtcod.BKGND_NONE,
        libtcod.CENTER,
        f"{label}: {val}/{maximum}",
    )


def render_all(
    con: libtcod.console.Console,
    panel: libtcod.console.Console,
    entities: list,
    player: object,
    game_map: object,
    fov_map: libtcod.map.Map,
    fov_recompute: bool,
    screen_width: int,
    screen_height: int,
    bar_width: int,
    panel_height: int,
    panel_y: int,
    colors: dict,
):
    """Wrapper funtion to make libtcod calls rendering all entities
    
    Arguments:
        con {libtcod.console.Console} -- target console
        panel {libtcod.console.Console} -- UI panel
        entities {list} -- list of entities to be drawn
        player {object} -- player object
        game_map {object} -- GameMap object
        fov_map {libtcod.map.Map} -- FoV map (what we see)
        fov_recompute {bool} -- flag controlling FoV calculation
        screen_width {int} -- screen width
        screen_height {int} -- screen height
        bar_width {int} -- Desired bar width
        panel_height {int} -- UI panel height
        panel_y {int} -- y position for the UI panel
        colors {dict} -- colors to be used for the map
    """
    if fov_recompute:
        # Draw all map tiles
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                if visible:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get("light_wall"), libtcod.BKGND_SET
                        )
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get("light_ground"), libtcod.BKGND_SET
                        )
                    game_map.tiles[x][y].explored = True
                # Else, checks if we have explored it yet
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get("dark_wall"), libtcod.BKGND_SET
                        )
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get("dark_ground"), libtcod.BKGND_SET
                        )

    # Draw all entities in the list from lowest to highest priority
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    render_bar(
        panel,
        1,
        1,
        bar_width,
        "HP",
        player.fighter.hp,
        player.fighter.max_hp,
        libtcod.light_red,
        libtcod.darker_red,
    )

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)


def clear_all(con: libtcod.console.Console, entities: list):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con: libtcod.console.Console, entity: object, fov_map: libtcod.map.Map):
    """Render given entity in the map
    
    Arguments:
        con {libtcod.console.Console} -- Target console
        entity {object} -- target entity to rendering
        fov_map {libtcod.map.Map} -- FoV map to determine visibility
    """
    # Checks if given entity is visible for player
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(
            con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE
        )


def clear_entity(con: libtcod.console.Console, entity: object):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, " ", libtcod.BKGND_NONE)

