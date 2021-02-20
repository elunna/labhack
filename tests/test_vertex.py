from src import vertex


def test_Vertex_init__label():
    v = vertex.Vertex('vertex')
    assert v.label == 'vertex'


def test_Vertex_init__edgelist_is_empty():
    v = vertex.Vertex('vertex')
    assert v.edgelist == []


def test_Vertex_init__visited_is_False():
    v = vertex.Vertex('vertex')
    assert v.visited is False


def test_Vertex_init__prev_vertex_is_None():
    v = vertex.Vertex('vertex')
    assert v.prev_vertex is None


def test_Vertex_init__cost_is_0():
    v = vertex.Vertex('vertex')
    assert v.cost == 0


def test_Vertex_connect__success_returns_True():
    start_v = vertex.Vertex('1')
    end_v = vertex.Vertex('2')
    assert start_v.connect(end_vertex=end_v, edge_weight=5)


def test_Vertex_connect__default_weight_is_0():
    start_v = vertex.Vertex('1')
    end_v = vertex.Vertex('2')
    start_v.connect(end_vertex=end_v)
    assert start_v.edgelist[0].weight == 0


def test_Vertex_connect__creates_Edge_in_edgelist():
    start_v = vertex.Vertex('1')
    end_v = vertex.Vertex('2')
    start_v.connect(end_vertex=end_v, edge_weight=5)
    assert len(start_v.edgelist) == 1


def test_Vertex_connect__edge_vertext():
    start_v = vertex.Vertex('1')
    end_v = vertex.Vertex('2')
    start_v.connect(end_vertex=end_v, edge_weight=5)
    edge = start_v.edgelist[0]
    assert edge.vertex == end_v


def test_Vertex_connect__same_vertices_returns_False():
    start_v = vertex.Vertex('1')
    assert start_v.connect(end_vertex=start_v, edge_weight=5) is False


def test_Vertex_connect__same_vertices__no_edge_added():
    start_v = vertex.Vertex('1')
    start_v.connect(end_vertex=start_v, edge_weight=5)
    assert len(start_v.edgelist) == 0


def test_Vertex_connect__dupe_edge_returns_False():
    start_v = vertex.Vertex('1')
    end_v = vertex.Vertex('2')
    start_v.connect(end_vertex=end_v, edge_weight=5)  # Add edge
    result = start_v.connect(end_vertex=end_v, edge_weight=5)  # Add again
    assert result is False


# get_weight_iter

def test_Vertex_has_neighbor():
    start_v = vertex.Vertex('1')
    assert start_v.has_neighbor() is False

    # Add a neighbor
    start_v.connect(end_vertex=vertex.Vertex('2'))
    assert start_v.has_neighbor()
