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
