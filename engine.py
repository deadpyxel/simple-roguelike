import tcod as libtcod


def main():
    # Screen size
    screen_width = 80
    screen_height = 50

    # Player initial position
    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    # Font settings
    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Creating screen
    libtcod.console_init_root(screen_width, screen_height, "Testing libtcod...", False)

    # input objects
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        # Capture input events
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # Initial screen config
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_put_char(0, player_x, player_y, "@", libtcod.BKGND_NONE)
        libtcod.console_flush()

        key = libtcod.console_check_for_keypress()
        # Exit on ESC
        if key.vk == libtcod.KEY_ESCAPE:
            return True


if __name__ == "__main__":
    main()
