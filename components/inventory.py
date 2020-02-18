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
