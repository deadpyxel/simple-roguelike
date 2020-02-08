import tcod as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all


def main():
    # Screen size
    screen_width = 80
    screen_height = 50
    # Map size
    map_width = 80
    map_height = 45
    # Room definitions
    max_rooms = 30
    room_min_size = 6
    room_max_size = 10
    # FoV configurations
    fov_algorithm = 0  # use defualt algorithm
    fov_light_walls = True  # light up walls we can see
    fov_radius = 10  # radius of view
    fov_recompute = True  # flag to trigger FoV computations
    # Define colors to be used in FoV
    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150),
        "light_wall": libtcod.Color(130, 110, 50),
        "light_ground": libtcod.Color(200, 180, 50),
    }
    # Font settings
    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Player initialization
    player = Entity(
        x=int(screen_width / 2), y=int(screen_height / 2), char="@", color=libtcod.white
    )
    # NPC initializatio
    npc = Entity(
        x=int(screen_width / 2 - 5),
        y=int(screen_height / 2),
        char="@",
        color=libtcod.yellow,
    )
    # Entity list
    entities = [player, npc]
    # Map object
    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size, player)

    # Fov map object
    fov_map = initialize_fov(game_map)

    # Creating screen
    libtcod.console_init_root(
        screen_width, screen_height, "Roguelike using libtcod", False
    )

    # Console object
    console = libtcod.console.Console(screen_width, screen_height)

    # input objects
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        # Capture input events
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # Trigger FoV calculation
        if fov_recompute == True:
            recompute_fov(
                fov_map, player.x, player.y, fov_radius, fov_light_walls, fov_algorithm
            )
        # Initial screen config
        render_all(
            con=console,
            entities=entities,
            game_map=game_map,
            fov_map=fov_map,
            fov_recompute=fov_recompute,
            screen_width=screen_width,
            screen_height=screen_height,
            colors=colors,
        )
        fov_recompute = False
        libtcod.console_flush()

        # Clear all entities
        clear_all(console, entities)

        # Capture action for given input
        action = handle_keys(key)
        # Map values for each input
        move = action.get("move")
        _exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        # Handle movement
        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)
                fov_recompute = True
        # Handle game exit
        if _exit:
            return True
        # toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
