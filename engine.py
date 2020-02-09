import tcod as libtcod

from components.fighter import Fighter
from death_handlers import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
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
    # Monster spawning settings
    max_monsters_per_room = 3
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
    fighter_component = Fighter(
        hp=30, defense=2, power=5
    )  # define a fighter component for the player
    player = Entity(
        0, 0, "@", libtcod.white, "Player", blocks=True, fighter=fighter_component
    )
    # World entity list
    entities = [player]
    # Map object
    game_map = GameMap(map_width, map_height)
    game_map.make_map(
        max_rooms,
        room_min_size,
        room_max_size,
        player,
        entities,
        max_monsters_per_room=max_monsters_per_room,
    )
    # Fov map object
    fov_map = initialize_fov(game_map)
    # Game state
    game_state = GameStates.PLAYERS_TURN

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
        player_turn_results = []

        # Handle movement. Check if this is players turn
        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            dest_x, dest_y = player.x + dx, player.y + dy
            if not game_map.is_blocked(dest_x, dest_y):
                target = get_blocking_entities_at_location(entities, dest_x, dest_y)
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                # Now it is enemies turn
                game_state = GameStates.ENEMY_TURN
        # Handle game exit
        if _exit:
            return True
        # toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Cycle through players action log
        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")

            if message:
                print(message)
            if dead_entity:
                if dead_entity == player:
                    message, game_state= kill_player(player)
                else:
                    message = kill_monster(dead_entity)
                print(message)

        # After all input is handle, check if this is enemies turn
        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities
                    )

                    # Cycle through players action log
                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get("message")
                        dead_entity = enemy_turn_result.get("dead")

                        if message:
                            print(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(player)
                            else:
                                message = kill_monster(dead_entity)
                            print(message)
                    # If player has died, no need to continue with enemies
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
