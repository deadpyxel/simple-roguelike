class Item:
    """Item class. Defines item component behaviour
    """

    def __init__(
        self,
        use_function: callable = None,
        targeting: bool = False,
        targeting_message: object = None,
        **kwargs
    ):
        """Item initializer
        
        Keyword Arguments:
            use_function {callable} -- function to be called on item use (default: {None})
            targeting {bool} -- controls if item needs targeting or not (default: {False})
            targeting_message {object} -- In case `targeting==True`, show this message when entering target mode (default: {None})
        """
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
