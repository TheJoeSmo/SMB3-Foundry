

class Proxy:
    """
    Pretends to be a target class and allows for additional actions to be taken
    """
    def __init__(self, target):
        self.target = target

    def __getattr__(self, name):
        return getattr(self.target, name)