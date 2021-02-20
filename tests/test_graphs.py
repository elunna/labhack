import pytest

from src.graphs import Graph, Edge


def test_Graph_init():
    g = Graph()
    assert g.edges == set()
    assert g.neighbors == {}


def test_Graph_init__vertices_arg():
    vertices = [1, 2, 3]
    g = Graph(vertices=vertices)
    assert g.neighbors == {1: set(), 2: set(), 3: set()}


def test_Graph_init__edges_arg():
    g = Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.edges == {frozenset({1, 2}), frozenset({2, 3})}


def test_Graph_add_vertex():
    g = Graph()
    g.add_vertex(1)
    assert 1 in g.neighbors


def test_Graph_add_vertex__success_returns_True():
    g = Graph()
    assert g.add_vertex(1)


def test_Graph_add_vertex__already_exists_returns_False():
    g = Graph(vertices=[1])
    assert g.add_vertex(1) is False


def test_Graph_add_edge__vertices_exist__adds_edge():
    g = Graph(vertices=[1, 2])
    g.add_edge(1, 2)
    assert g.edges == {frozenset({1, 2})}


def test_Graph_add_edge__vertices_exist__returns_True():
    g = Graph(vertices=[1, 2])
    assert g.add_edge(1, 2)


def test_Graph_add_edge__vertices_DNE__returns_False():
    g = Graph()
    assert not g.add_edge(1, 2)


def test_Graph_add_edge__edge_already_exists__returns_False():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert not g.add_edge(1, 2)


def test_Graph_rm_edge__edge_is_removed():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_edge(1, 2)
    assert frozenset([1, 2]) not in g.edges


def test_Graph_rm_edge__neighbors_are_removed():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.neighbors == {1: {2}, 2: {1}}
    g.rm_edge(1, 2)
    assert g.neighbors == {1: set(), 2: set()}


def test_Graph_rm_edge__success_returns_True():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_edge(1, 2)


def test_Graph_rm_edge__edge_DNE__returns_False():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_edge(3, 4) is False


def test_Graph_rm_vertex__vertex_is_removed():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_vertex(1)
    assert 1 not in g.neighbors


def test_Graph_rm_vertex__neighbors_are_removed():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_vertex(1)
    e = frozenset([1, 2])
    assert e not in g.edges


def test_Graph_rm_vertex__success_returns_True():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_vertex(1)


def test_Graph_rm_vertex__vertex_DNE_returns_False():
    g = Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_vertex(666) is False


def test_Graph_degree():
    g = Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.degree(1) == 1
    assert g.degree(2) == 2
    assert g.degree(3) == 1


def test_Graph_m_property():
    # m is the # of edges
    g = Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.m == len(g.edges)


def test_Graph_n_property():
    # n is the # of vertices
    g = Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.n == len(g.neighbors)


def test_Edge_init():
    e = Edge('u', 'v', weight=10)
    assert e.u == 'u'
    assert e.v == 'v'
    assert e.weight == 10


def test_Edge_init__default_weight_0():
    e = Edge('u', 'v')
    assert e.weight == 0


def test_Edge_init__same_vertices__raise_ValueError():
    with pytest.raises(ValueError):
        e = Edge('v', 'v')
