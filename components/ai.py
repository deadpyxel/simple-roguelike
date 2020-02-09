import tcod as libtcod


class BasicMonster:
    """Basic Monster behaviour component
    """

    def take_turn(self, target, fov_map, game_map, entities):
        """Handle turn
        """
        monster = self.owner
        # If the monster is in the FoV
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            # If the target is too far move towards it
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map, entities)
            # Else, attack
            elif target.fighter.hp > 0:
                print(f"The {monster.name} insults you! Your ego is damaged!")

