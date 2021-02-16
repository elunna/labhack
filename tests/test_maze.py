from src import maze


def test_Cell():
    c = maze.Cell()
    c.visited = False
    c.path_n = None
    c.path_s = None
    c.path_w = None
    c.path_e = None


def test_Maze_init__width_and_height():
    m = maze.Maze(width=10, height=10)
    assert m.width == 10
    assert m.height == 10


def test_Maze_init__maze_cells__initialized_to_Cells():
    m = maze.Maze(width=10, height=10)
    # Skip the first starting cell
    assert all(True for cell in m.maze if isinstance(cell, maze.Cell))


def test_Maze_init__maze_size():
    WIDTH = 10
    HEIGHT = 10
    m = maze.Maze(width=WIDTH, height=HEIGHT)
    assert len(m.maze) == WIDTH * HEIGHT


def test_Maze_init__stack_has_start_default():
    m = maze.Maze(width=10, height=10)
    assert m.stack == [(0, 0)]


def test_Maze_init__stack_has_custom_start():
    m = maze.Maze(width=10, height=10, start=(1, 1))
    assert m.stack == [(1, 1)]


def test_Maze_init__visited():
    m = maze.Maze(width=10, height=10)
    assert m.visited == 1


def test_Maze_init__first_cell_visited():
    m = maze.Maze(width=10, height=10)
    assert m.visited == 1


def test_Maze_init__path_width():
    m = maze.Maze(width=10, height=10)
    assert m.path_width == 3


def test_Maze_visited_property__1_on_init():
    m = maze.Maze(width=10, height=10)
    assert m.visited == 1


def test_Maze_visited_property():
    m = maze.Maze(width=10, height=10)
    m.maze[1].visited = True
    assert m.visited == 2


def test_Maze_get_cell__default_start():
    m = maze.Maze(width=10, height=10)
    # Start cell will be visited, so we can test that
    assert m.get_cell(0, 0).visited


def test_Maze_get_cell__different_start():
    m = maze.Maze(width=10, height=10, start=(5, 4))
    # Start cell will be visited, so we can test that
    assert m.get_cell(5, 4).visited
