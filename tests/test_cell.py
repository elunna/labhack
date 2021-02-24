from src import cell


def test_Cell():
    c = cell.Cell()
    c.visited = False
    c.path_n = None
    c.path_s = None
    c.path_w = None
    c.path_e = None
