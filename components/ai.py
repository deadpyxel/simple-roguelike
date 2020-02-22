from random import randint

import tcod as libtcod

from game_messages import Message


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


class ConfusedMonster:
    """Confused monster behaviour.
    """

    def __init__(self, previous_ai: BasicMonster, number_of_turns: int = 10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(
        self, target: object, fov_map: object, game_map: object, entities: list
    ):
        """For confused monsters, the turn consists of randomly moving or staying in place
        
        Arguments:
            target {object} -- [description]
            fov_map {object} -- [description]
            game_map {object} -- [description]
            entities {list} -- [description]
        
        Returns:
            [type] -- [description]
        """
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append(
                {
                    "message": Message(
                        f"The {self.owner.name} is no longer confused!", libtcod.red,
                    )
                }
            )

        return results

