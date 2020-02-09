import tcod as libtcod


class BasicMonster:
    """Basic Monster behaviour component
    """

    def take_turn(
        self, target: object, fov_map: object, game_map: object, entities: list
    ) -> list:
        """Turn action handling
        
        Arguments:
            target {object} -- target entity
            fov_map {object} -- FoV map
            game_map {object} -- GameMap object
            entities {list} -- List of entities in the map
        
        Returns:
            [list] -- resulting action log
        """
        results = []
        monster = self.owner
        # If the monster is in the FoV
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            # If the target is too far move towards it
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map, entities)
            # Else, attack
            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

