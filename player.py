class Player:
    """Abstract class that forces players to have a play method.
    """
    def __init__(self):
        raise NotImplementedError()

    def play(self, game):
        raise NotImplementedError()
