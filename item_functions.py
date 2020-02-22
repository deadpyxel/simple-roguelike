import tcod as libtcod

from game_messages import Message


def heal(*args, **kwargs) -> list:
    """Function used by items that heal
    
    Returns:
        list -- results of item usage
    """
    entity = args[0]
    amount = kwargs.get("amount")

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append(
            {
                "consumed": False,
                "message": Message("You are already at full health", libtcod.yellow),
            }
        )
    else:
        entity.fighter.heal(amount)
        results.append(
            {
                "consumed": True,
                "message": Message("Your wounds start to fell better", libtcod.green),
            }
        )
    return results


def get_closest_entity(
    origin: object, entities: list, max_range: int
) -> object or None:
    """Utility function to get closest entity given an origin entity
    
    Arguments:
        origin {object} -- origin entity
        entities {list} -- list of possible entities 
        max_range {int} -- Maximum range for entity detection
    
    Returns:
        object or None -- Closest entity, none if no entity is close enough 
    """
    target = None
    closest_distance = max_range + 1

    for entity in entities:
        distance = origin.distance_to(entity)
        if distance < closest_distance:
            target = entity
            closest_distance = distance
    return target


def cast_lighting(*args, **kwargs) -> list:
    caster = args[0]  # point of origin
    entities = kwargs.get("entities")  # list of possible entities
    fov_map = kwargs.get("fov_map")  # FOV map for target selection
    damage = kwargs.get("damage")  # spell damage
    maximum_range = kwargs.get("maximum_range")  # maximum range for the spell

    results = []

    # The only possible entities for targeting are ones
    # with fighting capabilities in the caster's FoV
    possible_targets = [
        entity
        for entity in entities
        if (
            entity.fighter
            and entity != caster
            and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)
        )
    ]

    target = get_closest_entity(caster, possible_targets, maximum_range)

    if target:
        results.append(
            {
                "consumed": True,
                "target": target,
                "message": Message(
                    f"A lighting bolt strikes the {target.name} with a loud thunder! The damage is {damage}"
                ),
            }
        )
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append(
            {
                "consumed": False,
                "target": None,
                "message": Message("No enemy is close enough to strike.", libtcod.red),
            }
        )

    return results

