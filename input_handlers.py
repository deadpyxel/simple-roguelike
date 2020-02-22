import tcod as libtcod

from game_states import GameStates


def handle_keys(key: libtcod.Key, game_state: GameStates) -> dict:
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.TARGET_MODE:
        return handle_targeting_keys(key)
    elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        return handle_inventory_keys(key)
    # No valid key was pressed
    return {}


def handle_player_turn_keys(key: libtcod.Key()) -> dict:
    """Handler for any keypress from the player on its turn
    
    Arguments:
        key {libtcod.Key} -- object containing keypress data
    
    Returns:
        dict -- dictionary describing action for input
    """
    key_ch = chr(key.c)  # capture key character
    # Movement keys
    if key.vk == libtcod.KEY_UP or key_ch == "k":
        return {"move": (0, -1)}
    elif key.vk == libtcod.KEY_DOWN or key_ch == "j":
        return {"move": (0, 1)}
    elif key.vk == libtcod.KEY_LEFT or key_ch == "h":
        return {"move": (-1, 0)}
    elif key.vk == libtcod.KEY_RIGHT or key_ch == "l":
        return {"move": (1, 0)}
    elif key_ch == "y":
        return {"move": (-1, -1)}
    elif key_ch == "u":
        return {"move": (1, -1)}
    elif key_ch == "b":
        return {"move": (-1, 1)}
    elif key_ch == "n":
        return {"move": (1, 1)}

    # Item pickup action
    elif key_ch == "g":
        return {"pickup": True}

    # Show inventory
    elif key_ch == "i":
        return {"show_inventory": True}
    # Drop inventory
    elif key_ch == "d":
        return {"drop_inventory": True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {"exit": True}

    # No valid key was pressed
    return {}


def handle_player_dead_keys(key: libtcod.Key()) -> dict:
    """Handler for any player keypress when dead
    
    Arguments:
        key {libtcod.Key} -- object containing keypress data
    
    Returns:
        dict -- dictionary describing action for input
    """
    key_ch = chr(key.c)  # capture key character

    # Show inventory
    if key_ch == "i":
        return {"show_inventory": True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {"exit": True}

    # No valid key was pressed
    return {}


def handle_inventory_keys(key: libtcod.Key()) -> dict:
    """Handler for any keypress when opening inventory
    
    Arguments:
        key {libtcod.Key} -- object containing keypress data
    
    Returns:
        dict -- dictionary describing action for input
    """
    index = key.c - ord("a")  # capture key character and get the index
    if index >= 0:
        return {"inventory_index": index}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {"exit": True}

    # No valid key was pressed
    return {}


def handle_targeting_keys(key:libtcod.Key) ->dict:
    """Handles keypresses in targeting mode.

    Only allows for ESC (exit).
    
    Arguments:
        key {libtcod.Key} -- Key press object
    
    Returns:
        dict -- actions to be taken given a keypress
    """    
    if key.vk== libtcod.KEY_ESCAPE:
        return {'exit': True}
    return {}

def handle_mouse(mouse:libtcod.Mouse)->dict:
    """Hendle mouse clicks
    
    Arguments:
        mouse {libtcod.Mouse} -- mouse listener object
    
    Returns:
        dict -- mouse actions
    """    
    (x, y) = (mouse.cx, mouse.cy)
    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}
    return {}