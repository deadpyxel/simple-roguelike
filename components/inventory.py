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

