import tcod as libtcod

from game_messages import Message


class Inventory:
    """Inventory class. Defines Inventory logic and behaviour
    """

    def __init__(self, capacity: int):
        """Inventory initializer.
        
        Arguments:
            capacity {int} -- Determinates how many items you cna hold
        """
        self.capacity = capacity
        self.items = []  # Container that holds the items

    def add_item(self, item: object) -> list:
        """Item add behaviour. Adds an item to inventory if
        not over capacity, else does not pick up item and
        warns the player
        
        Arguments:
            item {object} -- Item object to be picked up
        
        Returns:
            list -- list of game messages resulting from player's actions
        """
        results = []

        if len(self.items) >= self.capacity:
            results.append(
                {
                    "item_added": None,
                    "message": Message(
                        "You cannot carry any more, your inventory is full!",
                        color=libtcod.yellow,
                    ),
                }
            )
        else:
            results.append(
                {
                    "item_added": item,
                    "message": Message(
                        f"You pickup a {item.name}", color=libtcod.blue,
                    ),
                }
            )
            self.items.append(item)

        return results

    def remove_item(self, item: object):
        """Remove an item from the inventory
        
        Arguments:
            item {object} -- Item to be removed
        """
        self.items.remove(item)

    def use(self, item_entity: object, **kwargs) -> list:
        """Use an item from the inventory.

        The keyword args provided will be used by the `item_use` function
        
        Arguments:
            item_entity {object} -- Item to be used
        
        Returns:
            list -- list of resulting actions from item usage
        """
        results = []

        item_component = item_entity.item

        # Check if the item is usable
        if item_component.use_function is None:
            results.append(
                {
                    "message": Message(
                        f"The {item_entity.name} cannot be used", color=libtcod.yellow
                    )
                }
            )
        else:
            kwargs = {**item_component.function_kwargs, **kwargs}
            item_use_results = item_component.use_function(self.owner, **kwargs)
            for result in item_use_results:
                if result.get("consumed"):
                    # Once item has been used, remove from inventory
                    self.remove_item(item_entity)

            results.extend(item_use_results)

        return results
