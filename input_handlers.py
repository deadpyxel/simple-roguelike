import tcod as libtcod


def handle_keys(key: libtcod.Key()) -> dict:
    """Handler for any keypress
    
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
    if key_ch == "g":
        return {"pickup": True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {"fullscreen": True}

    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {"exit": True}

    # No key was pressed
    return {}
