DIRECTIONS = [
    (0, -1),  # North
    (-1, 0),  # West
    (1, 0),  # East
    (0, 1),  # South
]


class Cell:
    def __init__(self):
        self.visited = False
        self.path_n = None
        self.path_s = None
        self.path_w = None
        self.path_e = None


class Maze:
    """ This is the constructor for a 2D maze. """
    def __init__(self, width, height, start=(0, 0)):
        self.width = width
        self.height = height

        """ Options for maze construction
            1. Simple 1D list of ints 
            2. 2D array
            3. Dict: points and lists (of neighbors?)
        """

        # Initialize with Cell objects
        self.maze = [Cell() for _ in range(self.width * self.height)]

        self.stack = []  # Contains (x, y) pairs

        # Set first start cell
        self.stack.append(start)
        self.get_cell(*start).visited = True

        """ For us to represent the maze cells onto a console grid, we need to account for path "walls"
            By using a path width of 3, we can bake that in without creating any more work.
            if C represents the cell, and | is the wall, each "Cell" is effectively translated like this: 
                CC|
                CC|
                |||
            
            We only need to be concerned with digging on the eastern and southern walls.
            The relationship to the console is: 
                (Cell Coordinate * 2) + 1
        """
        self.path_width = 3

    @property
    def visited(self):
        return sum(1 for c in self.maze if c.visited)

    def get_cell(self, x, y):
        return self.maze[self.width * y + x]

    def draw(self):
        # Initialize console to all walls
        console = [
            ['#' for y in range(self.height * self.path_width)]
            for x in range(self.width * self.path_width)
        ]

        for x in range(self.width):
            for y in range(self.height):
                if self.get_cell(x, y).visited:
                    console[x * (self.path_width + 1)][y] = '.'

        for y in console:
            print(''.join(y))


if __name__ == "__main__":
    m = Maze(width=10, height=10)
    m.draw()
