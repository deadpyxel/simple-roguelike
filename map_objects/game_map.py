from random import randint

import tcod as libtcod

from entity import Entity
from map_objects.tile import Tile
from map_objects.room import Room


class GameMap:
    """GameMap class. instantiate a GameMap with a tile grid
    """

    def __init__(self, width: int, height: int):
        """GameMap initializer
        
        Arguments:
            width {int} -- map width
            height {int} -- map height
        """
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self) -> list:
        """Initialize the tile map
        
        Returns:
            list -- tile grid
        """
        # Initialize the WxH tile grid with non-blocking tiles
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(
        self,
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        player: object,
        entities: list,
        max_monsters_per_room: int = 5,
    ):
        """Create a map spawning random rooms as much as possible
        
        Arguments:
            max_rooms {int} -- maximum number of rooms
            room_min_size {int} -- minimum size for a room
            room_max_size {int} -- maximum size for a room
            player {object} -- Player entity
            entities {list} -- World entities list
            max_monsters_per_room {int} -- Limit of monsters per room (Default: 5)
        """
        rooms = []
        num_rooms = 0

        for _ in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # Get a random position respecting boundaries
            x = randint(0, self.width - w - 1)
            y = randint(0, self.height - h - 1)

            # Create a random room
            new_room = Room(x, y, w, h)
            # If it intersects any other room, skip
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # No intersections found
                self.create_room(new_room)
                # Get the center of the room
                (center_x, center_y) = new_room.center()
                if num_rooms == 0:
                    # this is the first room, spawn the player
                    player.x = center_x
                    player.y = center_y
                else:
                    # after the first room
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()
                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, center_x, prev_y)
                        self.create_v_tunnel(prev_y, center_y, center_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, center_y, prev_x)
                        self.create_h_tunnel(prev_x, center_x, center_y)
                # Spawn entities in this room
                self.place_entities(new_room, entities, max_monsters_per_room)
                # save the created room to a list
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room: Room):
        """Carve out a room in the GameMap
        
        Arguments:
            room {Room} -- room object containing dimensions for the room
        """
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1: int, x2: int, y: int):
        """Define a horizontal tunnel
        
        Arguments:
            x1 {int} -- start of the tunnel
            x2 {int} -- end of the tunnel
            y {int} -- y position related to gamemap
        """
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1: int, y2: int, x: int):
        """Define a vertical tunnel
        
        Arguments:
            y1 {int} -- start of the tunnel
            y2 {int} -- end of the tunnel
            x {int} -- x position related to gamemap
        """
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room: Room, entities: list, max_monsters_per_room: int):
        # Get a random number of monsters for the room
        num_monsters = randint(0, max_monsters_per_room)

        for _ in range(num_monsters):
            # Choose random location for spawn
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if there's already an entity there
            if not any(
                [entity for entity in entities if entity.x == x and entity.y == y]
            ):
                # 80% of chance to spawn an Orc, else a Troll
                if randint(0, 100) < 80:
                    monster = Entity(x, y, "o", libtcod.desaturated_green, 'Orc', blocks=True)
                else:
                    monster = Entity(x, y, "T", libtcod.darker_green, 'Troll', blocks=True)

                entities.append(monster)

    def is_blocked(self, x: int, y: int) -> bool:
        """Checks if given map position is blocked
        
        Arguments:
            x {int} -- x position
            y {int} -- y position
        
        Returns:
            bool -- Blocking state of target tile
        """
        return self.tiles[x][y].blocked
