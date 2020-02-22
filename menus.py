import tcod as libtcod


def menu(
    con: libtcod.console.Console,
    header: str,
    options: list,
    width: int,
    screen_width: int,
    screen_height: int,
):
    """Generic Menu rendering function.
    
    Arguments:
        con {libtcod.console.Console} -- Target console to show the menu
        header {str} -- header (description) for the menu
        options {list} -- lsit of options for the menu
        width {int} -- desired width of the menu
        screen_width {int} -- limit screen width 
        screen_height {int} -- limit screen height
    
    Raises:
        ValueError: if list of `options` has more than 26 members
    """
    if len(options) > 26:
        raise ValueError("Cannot have a menu with more than 26 options.")

    # calculate total height for the header (after auto-wrap), one line per option
    header_height = libtcod.console_get_height_rect(
        con, 0, 0, width, screen_height, header
    )
    height = len(options) + header_height

    # Off screen console fo the menu's window
    window = libtcod.console_new(width, height)

    # Render the header
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(
        window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header
    )

    # Render all options
    y = header_height
    letter_index = ord("a")
    for option_text in options:
        text = f"({chr(letter_index)}) {option_text}"
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(
    con: libtcod.console.Console,
    header: str,
    inventory: object,
    inventory_width: int,
    screen_width: int,
    screen_height: int,
):
    # Generate menu options
    if len(inventory.items) == 0:
        options = ["Inventory is empty"]
    else:
        options = [item.name for item in inventory.items]

    menu(con, header, options, inventory_width, screen_width, screen_height)
