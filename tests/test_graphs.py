from src.graphs import Graph


def test_Graph_init():
    g = Graph()
    assert g.edges == set()
    assert g.neighbors == {}


def test_Graph_init__vertices_arg():
    vertices = [1, 2, 3]
    g = Graph(vertices=vertices)
    assert g.neighbors == {1: set(), 2: set(), 3: set()}


def test_Graph_init__edges_arg():
    edges = {(1, 2), (2, 3)}
    g = Graph(edges=edges)
    assert g.edges == {frozenset({1, 2}), frozenset({2, 3})}


def test_Graph_init__edges__add_vertices():
    edges = {(1, 2), (2, 3)}
    g = Graph(edges=edges)

    assert g.neighbors == {
        1: {2},
        2: {1, 3},
        3: {2}
    }


def test_add_vertex():
    g = Graph()
    g.add_vertex(1)
    assert 1 in g.neighbors


def test_add_vertex__success_returns_True():
    g = Graph()
    assert g.add_vertex(1)


def test_add_vertex__already_exists_returns_False():
    g = Graph(vertices=[1])
    assert g.add_vertex(1) is False


