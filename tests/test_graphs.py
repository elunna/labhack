import pytest

from src import graphs


def test_Graph_init():
    g = graphs.Graph()
    assert g.edges == set()
    assert g.neighbors == {}


def test_Graph_init__vertices_arg():
    vertices = [1, 2, 3]
    g = graphs.Graph(vertices=vertices)
    assert g.neighbors == {1: set(), 2: set(), 3: set()}


def test_Graph_init__edges_arg():
    g = graphs.Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.edges == {frozenset({1, 2}), frozenset({2, 3})}


def test_Graph_add_vertex():
    g = graphs.Graph()
    g.add_vertex(1)
    assert 1 in g.neighbors


def test_Graph_add_vertex__success_returns_True():
    g = graphs.Graph()
    assert g.add_vertex(1)


def test_Graph_add_vertex__already_exists_returns_False():
    g = graphs.Graph(vertices=[1])
    assert g.add_vertex(1) is False


def test_Graph_has_edge__edge_DNE():
    g = graphs.Graph(vertices=[1, 2])
    assert g.has_edge(2, 3) is False


def test_Graph_has_edge__edge_exists():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.has_edge(1, 2)


def test_Graph_add_edge__vertices_exist__adds_edge():
    g = graphs.Graph(vertices=[1, 2])
    g.add_edge(1, 2)
    assert g.edges == {frozenset({1, 2})}


def test_Graph_add_edge__vertices_exist__returns_True():
    g = graphs.Graph(vertices=[1, 2])
    assert g.add_edge(1, 2)


def test_Graph_add_edge__vertices_DNE__returns_False():
    g = graphs.Graph()
    assert not g.add_edge(1, 2)


def test_Graph_add_edge__edge_already_exists__returns_False():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert not g.add_edge(1, 2)


def test_Graph_rm_edge__edge_is_removed():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_edge(1, 2)
    assert frozenset([1, 2]) not in g.edges


def test_Graph_rm_edge__neighbors_are_removed():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.neighbors == {1: {2}, 2: {1}}
    g.rm_edge(1, 2)
    assert g.neighbors == {1: set(), 2: set()}


def test_Graph_rm_edge__success_returns_True():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_edge(1, 2)


def test_Graph_rm_edge__edge_DNE__returns_False():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_edge(3, 4) is False


def test_Graph_rm_vertex__vertex_is_removed():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_vertex(1)
    assert 1 not in g.neighbors


def test_Graph_rm_vertex__neighbors_are_removed():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    g.rm_vertex(1)
    e = frozenset([1, 2])
    assert e not in g.edges


def test_Graph_rm_vertex__success_returns_True():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_vertex(1)


def test_Graph_rm_vertex__vertex_DNE_returns_False():
    g = graphs.Graph(vertices=[1, 2], edges={(1, 2)})
    assert g.rm_vertex(666) is False


def test_Graph_degree():
    g = graphs.Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.degree(1) == 1
    assert g.degree(2) == 2
    assert g.degree(3) == 1


def test_Graph_m_property():
    # m is the # of edges
    g = graphs.Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.m == len(g.edges)


def test_Graph_n_property():
    # n is the # of vertices
    g = graphs.Graph(vertices=[1, 2, 3], edges={(1, 2), (2, 3)})
    assert g.n == len(g.neighbors)


def test_Edge_init():
    e = graphs.Edge('u', 'v', weight=10)
    assert e.u == 'u'
    assert e.v == 'v'
    assert e.weight == 10


def test_Edge_init__default_weight_0():
    e = graphs.Edge('u', 'v')
    assert e.weight == 0


def test_Edge_init__same_vertices__raise_ValueError():
    with pytest.raises(ValueError):
        e = graphs.Edge('v', 'v')


def test_dfs__no_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c'])
    result = g.dfs('a')
    assert result == {'a': None}


def test_dfs__1_edge():
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=['ab'])
    result = g.dfs('a')
    assert result == {'a': None, 'b': 'a'}


def test_dfs__2_edges():
    edges = 'ab bc'.split()
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=edges)
    result = g.dfs('a')
    assert result == {'a': None, 'b': 'a', 'c': 'b'}


@pytest.mark.skip(reason='Set randomness makes this difficult to test.')
def test_dfs__4_edges():
    edges = 'ab bc bd cd'.split()
    g = graphs.Graph(vertices=['a', 'b', 'c', 'd'], edges=edges)
    result = g.dfs('a')
    assert result == {'a': None, 'b': 'a', 'c': 'b', 'd': 'c'}


def test_connected__valid_connection_2_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=['ab', 'bc'])
    assert g.connected('a', 'c')


def test_connected__valid_connection_3_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c', 'd'], edges=['ab', 'bc', 'cd'])
    assert g.connected('a', 'd')


def test_connected__invalid_connection():
    g = graphs.Graph(vertices=['a', 'b', 'c', 'd'], edges=['ab', 'bc'])
    assert g.connected('a', 'd') is False


def test_path__2_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=['ab', 'bc'])
    assert g.path('a', 'c') == ['a', 'b', 'c']


def test_path__3_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c', 'd'], edges=['ab', 'bc', 'cd'])
    assert g.path('a', 'd') == ['a', 'b', 'c', 'd']


def test_bfs__no_edges():
    g = graphs.Graph(vertices=['a', 'b', 'c'])
    result = g.bfs('a')
    assert result == {'a': None}


def test_bfs__1_edge():
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=['ab'])
    result = g.bfs('a')
    assert result == {'a': None, 'b': 'a'}


def test_bfs__2_edges():
    edges = 'ab bc'.split()
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=edges)
    result = g.bfs('a')
    assert result == {'a': None, 'b': 'a', 'c': 'b'}


def test_bfs__3_edges():
    edges = 'ab ac bc'.split()
    g = graphs.Graph(vertices=['a', 'b', 'c'], edges=edges)
    result = g.bfs('a')
    assert result == {'a': None, 'b': 'a', 'c': 'a'}
