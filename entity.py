import math

import tcod as libtcod


class Entity:
    """A generic class used to represent player, npcs, enemies
    """

    def __init__(
        self,
        x: int,
        y: int,
        char: str,
        color: object,
        name: str,
        blocks: bool = False,
        fighter: object = None,
        ai: object = None,
    ):
        """Entity initializer
        
        Arguments:
            x {int} -- initial X position
            y {int} -- initial y position
            char {str} -- Character to represent entity
            color {object} -- Color objet used to color character on screen 
            name {str} -- Name of the entity
        Keyword Arguments:
            blocks {bool} -- Block behaviour flag (default: {False})
            fighter {object} -- fighting component (default: {None})
            ai {object} -- AI component (default: {None})
        """
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        self.ai = ai

        # If components are present, set this entity as owner
        if self.fighter:
            self.fighter.owner = self
        if self.ai:
            self.ai.owner = self

    def move(self, dx: int, dy: int):
        """Move entity by given amount
        
        Arguments:
            dx {int} -- adjustment on X axis
            dy {int} -- adjustment on Y axis
        """
        self.x += dx
        self.y += dy

    def move_towards(
        self, target_x: int, target_y: int, game_map: object, entities: list
    ):
        """Move this entity towards a target position
        
        Arguments:
            target_x {int} -- x position of target
            target_y {int} -- y position of target
            game_map {object} -- GameMap object
            entities {list} -- list of entities in the map
        """
        dx = target_x - self.x  # delta x
        dy = target_y - self.y  # delta y
        dist = math.sqrt(dx ** 2 + dy ** 2)  # Euclidian distance

        dx = int(round(dx / dist))
        dy = int(round(dy / dist))

        if not (
            game_map.is_blocked(self.x + dx, self.y + dy)
            or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)
        ):
            self.move(dx, dy)

    def move_astar(self, target: object, game_map: object, entities: list):
        """Use A* algorithm to move towards a target
        
        Arguments:
            target {object} -- target Entity object
            game_map {object} -- Gamemap object
            entities {list} -- list of entities in the map
        """
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map.Map(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(
                    fov,
                    x1,
                    y1,
                    not game_map.tiles[x1][y1].block_sight,
                    not game_map.tiles[x1][y1].blocked,
                )

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)

    def distance_to(self, other: object) -> int or float:
        """Returns distance between entitities
        
        Arguments:
            other {Entity} -- other entity to check
        
        Returns:
            int or float -- euclidian distance between entities
        """
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
