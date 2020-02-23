import tcod as libtcod

from components import Fighter, Inventory, Item
from entity import Entity
from game_messages import MessageLog
from game_states import GameStates
from map_objects import GameMap
from render_functions import RenderOrder


def get_color_settings() -> dict:
    colors = {
        "dark_wall": libtcod.Color(0, 0, 100),
        "dark_ground": libtcod.Color(50, 50, 150),
        "light_wall": libtcod.Color(130, 110, 50),
        "light_ground": libtcod.Color(200, 180, 50),
    }

    return colors


def get_game_settings() -> dict:
    # Map size
    map_width = 80
    map_height = 43
    # Room definitions
    max_rooms = 30
    room_min_size = 6
    room_max_size = 10
    # FoV configurations
    fov_algorithm = 0  # use defualt algorithm
    fov_light_walls = True  # light up walls we can see
    fov_radius = 10  # radius of view
    # Monster spawning settings
    max_monsters_per_room = 3
    max_items_per_room = 2

    game_settings = {
        "map_width": map_width,
        "map_height": map_height,
        "room_max_size": room_max_size,
        "room_min_size": room_min_size,
        "max_rooms": max_rooms,
        "fov_algorithm": fov_algorithm,
        "fov_light_walls": fov_light_walls,
        "fov_radius": fov_radius,
        "max_monsters_per_room": max_monsters_per_room,
        "max_items_per_room": max_items_per_room,
    }

    return game_settings


def get_ui_settings() -> dict:
    # Screen size
    screen_width = 80
    screen_height = 50
    # UI settings
    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height
    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    ui_settings = {
        "screen_width": screen_width,
        "screen_height": screen_height,
        "bar_width": bar_width,
        "panel_height": panel_height,
        "panel_y": panel_y,
        "message_x": message_x,
        "message_width": message_width,
        "message_height": message_height,
    }

    return ui_settings


def get_configuration_params() -> dict:
    window_title = "Simple-Roguelike: An adventure by libtcod"

    ui_settings = get_ui_settings()
    game_settings = get_game_settings()
    # Define colors to be used in FoV
    colors = get_color_settings()

    constants = {
        "window_title": window_title,
        "ui_settings": ui_settings,
        "game_settings": game_settings,
        "colors": colors,
    }

    return constants


def initialize_game_map(configs: dict, player: Entity, entities: list) -> GameMap:
    # Map object
    game_map = GameMap(configs["map_width"], configs["map_height"])
    game_map.make_map(
        configs["max_rooms"],
        configs["room_min_size"],
        configs["room_max_size"],
        player,
        entities,
        max_monsters_per_room=configs["max_monsters_per_room"],
    )

    return game_map


def get_game_objects(configs: dict) -> list:
    game_settings = configs["game_settings"]
    ui_settings = configs["ui_settings"]
    fighter_component = Fighter(
        hp=30, defense=2, power=5
    )  # define a fighter component for the player
    inventory_component = Inventory(26)  # Inventory component for the player
    player = Entity(
        0,
        0,
        "@",
        libtcod.white,
        "Player",
        blocks=True,
        render_order=RenderOrder.ACTOR,
        fighter=fighter_component,
        inventory=inventory_component,
    )
    # World entity list
    entities = [player]
    # Map object
    game_map = initialize_game_map(game_settings, player, entities)
    # Message Log object
    message_log = MessageLog(
        ui_settings["message_x"],
        ui_settings["message_width"],
        ui_settings["message_height"],
    )
    # Game state
    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
