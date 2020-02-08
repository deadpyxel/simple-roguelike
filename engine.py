import tcod as libtcod

from entity import Entity
from input_handlers import handle_keys


def main():
    # Screen size
    screen_width = 80
    screen_height = 50

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

    # Font settings
    libtcod.console_set_custom_font(
        "arial10x10.png", libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD
    )

    # Creating screen
    libtcod.console_init_root(screen_width, screen_height, "Testing libtcod...", False)

    # Console object
    console = libtcod.console_new(screen_width, screen_height)

    # input objects
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # Game loop
    while not libtcod.console_is_window_closed():
        # Capture input events
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # Initial screen config
        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_put_char(console, player.x, player.y, "@", libtcod.BKGND_NONE)
        libtcod.console_blit(console, 0, 0, screen_width, screen_height, 0, 0, 0)
        libtcod.console_flush()

        libtcod.console_put_char(console, player.x, player.y, " ", libtcod.BKGND_NONE)

        # Capture action for given input
        action = handle_keys(key)
        # Map values for each input
        move = action.get("move")
        _exit = action.get("exit")
        fullscreen = action.get("fullscreen")

        # Handle movement
        if move:
            dx, dy = move
            player.move(dx, dy)
        # Handle game exit
        if _exit:
            return True
        # toggle fullscreen
        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


if __name__ == "__main__":
    main()
