from src.directed_graph import DirectedGraph

import pytest


@pytest.fixture
def test_graph():
    g = DirectedGraph()
    g.add_vertex('a')
    g.add_vertex('b')
    return g


def test_DirectedGraph_init__vertices_is_empty_dict():
    g = DirectedGraph()
    assert g.vertices == {}


def test_DirectedGraph_init__edgecount_is_0():
    g = DirectedGraph()
    assert g.edge_count == 0


def test_DirectedGraph_add_vertex__success_returns_True():
    g = DirectedGraph()
    assert g.add_vertex('a')


def test_DirectedGraph_add_vertex__vertex_added():
    g = DirectedGraph()
    g.add_vertex('a')
    assert 'a' in g.vertices


def test_DirectedGraph_add_vertex__dupe_vertex_returns_False():
    g = DirectedGraph()
    g.add_vertex('a')
    assert g.add_vertex('a') is False


def test_DirectedGraph_add_edge__begin_DNE_returns_False():
    g = DirectedGraph()
    g.add_vertex('b')
    assert g.add_edge(begin='a', end='b') is False


def test_DirectedGraph_add_edge__end_DNE_returns_False():
    g = DirectedGraph()
    g.add_vertex('a')
    assert g.add_edge(begin='a', end='b') is False


def test_DirectedGraph_add_edge__success_returns_True(test_graph):
    assert test_graph.add_edge(begin='a', end='b')


def test_DirectedGraph_add_edge__success__edgecount_increased(test_graph):
    test_graph.add_edge(begin='a', end='b')
    assert len(test_graph.vertices['a'].edgelist) == 1


def test_DirectedGraph_add_edge__success_begin_has_end_vertex(test_graph):
    test_graph.add_edge(begin='a', end='b')
    edge = test_graph.vertices['a'].edgelist[0]
    assert edge.vertex == test_graph.vertices['b']  # edge has the ending vertex


def test_DirectedGraph_add_edge__default_weight_is_0(test_graph):
    test_graph.add_edge(begin='a', end='b')
    edge = test_graph.vertices['a'].edgelist[0]
    assert edge.weight == 0


def test_DirectedGraph_add_edge__set_weight(test_graph):
    test_graph.add_edge(begin='a', end='b', weight=10)
    edge = test_graph.vertices['a'].edgelist[0]
    assert edge.weight == 10


def test_DirectedGraph_has_edge__edge_exists_returns_True(test_graph):
    test_graph.add_edge(begin='a', end='b', weight=10)
    assert test_graph.has_edge('a', 'b')


def test_DirectedGraph_has_edge__DNE_returns_False(test_graph):
    assert test_graph.has_edge('a', 'b') is False


def test_DirectedGraph_is_empty__empty_returns_True():
    g = DirectedGraph()
    assert g.is_empty()


def test_DirectedGraph_is_empty__not_empty_returns_False(test_graph):
    assert test_graph.n > 0
    assert test_graph.is_empty() is False


def test_DirectedGraph_m_property__empty_graph_returns_0():
    g = DirectedGraph()
    assert g.m == 0


def test_DirectedGraph_m_property__1_edge(test_graph):
    test_graph.add_edge(begin='a', end='b', weight=10)
    assert test_graph.edge_count == 1
    assert test_graph.m == 1


def test_DirectedGraph_n_property__empty_graph_returns_0():
    g = DirectedGraph()
    assert g.n == 0


def test_DirectedGraph_n_property__2_verticies(test_graph):
    assert len(test_graph.vertices) == 2
    assert test_graph.n == 2


def test_DirectedGraph_clear__empty_graph():
    g = DirectedGraph()
    g.clear()
    assert g.is_empty()


def test_DirectedGraph_clear__non_empty_graph(test_graph):
    test_graph.clear()
    assert test_graph.is_empty()


def test_DirectedGraph_bft__1_edge(test_graph):
    test_graph.add_edge(begin='a', end='b')
    result = test_graph.bft('a')
    assert result == ['a', 'b']


def test_DirectedGraph_bft__2_edges(test_graph):
    test_graph.add_vertex('c')
    test_graph.add_edge(begin='a', end='b')
    test_graph.add_edge(begin='b', end='c')

    result = test_graph.bft('a')
    assert result == ['a', 'b', 'c']


def test_DirectedGraph_bft__3_edges__deep(test_graph):
    test_graph.add_vertex('c')
    test_graph.add_vertex('d')
    test_graph.add_edge(begin='a', end='b')
    test_graph.add_edge(begin='b', end='c')
    test_graph.add_edge(begin='c', end='d')

    result = test_graph.bft('a')
    assert result == ['a', 'b', 'c', 'd']


def test_DirectedGraph_bft__3_edges__shallow(test_graph):
    test_graph.add_vertex('c')
    test_graph.add_vertex('d')
    test_graph.add_edge(begin='a', end='b')
    test_graph.add_edge(begin='a', end='c')
    test_graph.add_edge(begin='a', end='d')

    result = test_graph.bft('a')
    assert result == ['a', 'b', 'c', 'd']