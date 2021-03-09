from src.directed_graph import Edge


def test_init__vertex():
    e = Edge(end_vertex='V', weight=10)
    assert e.vertex == 'V'


def test_init__weight():
    e = Edge(end_vertex='V', weight=10)
    assert e.weight == 10
