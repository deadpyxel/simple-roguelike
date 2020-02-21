class Item:
    """Item class. Defines item component behaviour
    """

    def __init__(self, use_function=None, **kwargs):
        self.use_function = use_function
        self.function_kwargs = kwargs
