

class UninitializedStateException(AttributeError):
    """
    An error for a state not being initialized
    """
    def __init__(self):
        super().__init__("State not initialized")
