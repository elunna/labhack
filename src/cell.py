class Cell:
    """This is a Cell in a maze, to aid in the generation of maze maps."""
    def __init__(self):
        self.visited = False
        self.path_n = None
        self.path_s = None
        self.path_w = None
        self.path_e = None
