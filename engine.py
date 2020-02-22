import tcod as libtcod

from death_handlers import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from game_messages import Message
from input_handlers import handle_keys, handle_mouse
from loaders.initializers import get_configuration_params, get_game_objects
from render_functions import clear_all, render_all, RenderOrder


def main():
    config_params = get_configuration_params()
    ui_settings = config_params.get("ui_settings")
    game_settings = config_params.get("game_settings")
    colors = config_params.get("colors")
    player, entities, game_map, message_log, game_state = get_game_objects(
        config_params
    )

    fov_recompute = True  # flag to trigger FoV computations

    # Font settings
    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Fov map object
    fov_map = initialize_fov(game_map)
    # Game state
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    # For item targeting
    targeting_item = None

    # Creating screen
    libtcod.console_init_root(
        ui_settings["screen_width"],
        ui_settings["screen_height"],
        config_params["window_title"],
        False,
    )

    # Console object
    console = libtcod.console.Console(
        ui_settings["screen_width"], ui_settings["screen_height"]
    )
    # Panel object
    panel = libtcod.console.Console(
        ui_settings["screen_width"], ui_settings["panel_height"]
    )

    # input objects
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        # Capture input events
        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse
        )
        # Trigger FoV calculation
        if fov_recompute == True:
            recompute_fov(
                fov_map,
                player.x,
                player.y,
                game_settings["fov_radius"],
                game_settings["fov_light_walls"],
                game_settings["fov_algorithm"],
            )
        # Initial screen config
        render_all(
            con=console,
            panel=panel,
            entities=entities,
            player=player,
            game_map=game_map,
            fov_map=fov_map,
            fov_recompute=fov_recompute,
            message_log=message_log,
            screen_width=ui_settings["screen_width"],
            screen_height=ui_settings["screen_height"],
            bar_width=ui_settings["bar_width"],
            panel_height=ui_settings["panel_height"],
            panel_y=ui_settings["panel_y"],
            mouse=mouse,
            colors=colors,
            gs=game_state,
        )
        fov_recompute = False
        libtcod.console_flush()

        # Clear all entities
        clear_all(console, entities)

        # Capture action for given input
        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)
        # Map values for each action
        move = action.get("move")
        pickup = action.get("pickup")
        show_inventory = action.get("show_inventory")
        drop_inventory = action.get("drop_inventory")
        inv_index = action.get("inventory_index")
        left_click = mouse_action.get("left_click")
        right_click = mouse_action.get("right_click")
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
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(
                    Message("There's nothing to pickup", color=libtcod.yellow)
                )
        # Show player inventory
        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY
        # Drop item dialog
        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY
        if (
            inv_index is not None
            and previous_game_state != GameStates.PLAYER_DEAD
            and inv_index < len(player.inventory.items)
        ):
            item = player.inventory.items[inv_index]
            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(
                    player.inventory.use(item, entities=entities, fov_map=fov_map)
                )
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))
        if game_state == GameStates.TARGET_MODE:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(
                    targeting_item,
                    entities=entities,
                    fov_map=fov_map,
                    target_x=target_x,
                    target_y=target_y,
                )

                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({"targeting_cancelled": True})
        # Handle game exit
        if _exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGET_MODE:
                player_turn_results.append({"targeting_cancelled": True})
            else:
                return True
        # toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # Cycle through players action log
        for player_turn_result in player_turn_results:
            message = player_turn_result.get("message")
            dead_entity = player_turn_result.get("dead")
            item_added = player_turn_result.get("item_added")
            item_consumed = player_turn_result.get("consumed")
            item_dropped = player_turn_result.get("item_dropped")
            targeting = player_turn_result.get("targeting")
            cancelled_targeting = player_turn_result.get("targeting_cancelled")

            if message:
                message_log.add_message(message)
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(player)
                else:
                    message = kill_monster(dead_entity)
                message_log.add_message(message)
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                game_state = GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGET_MODE
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)
            if cancelled_targeting:
                game_state = previous_game_state
                player_turn_result.get("targeting")

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
                            message_log.add_message(message)
                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(player)
                            else:
                                message = kill_monster(dead_entity)
                            message_log.add_message(message)
                    # If player has died, no need to continue with enemies
                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == "__main__":
    main()
