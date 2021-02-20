class Graph:
    """ Undirected graph: Implemented using an adjacency list
        edges: A set of frozen sets of 2 connected vertices.
        neighbors: A dict of Vertices as keys and sets of neighbors as values.
    """
    def __init__(self, vertices=None, edges=None):
        # Safeguard against mutable args
        if edges is None:
            edges = set()
        if vertices is None:
            vertices = []

        self.neighbors = {}
        for v in vertices:
            self.add_vertex(v)

        self.edges = set()
        for u, v in edges:
            self.add_edge(u, v)

    def add_vertex(self, v):
        if v not in self.neighbors:
            self.neighbors[v] = set()
            return True
        return False

    # TODO: Add has_edge(u, v)

    def add_edge(self, u, v):
        # The vertices must exist for the edge to be formed
        if u not in self.neighbors or v not in self.neighbors:
            return False

        e = frozenset([u, v])
        # The edge must not already exist in the graph.
        if e not in self.edges:
            self.edges.add(e)
            self.neighbors[u].add(v)
            self.neighbors[v].add(u)
            return True
        return False

    def rm_edge(self, u, v):
        e = frozenset([u, v])
        if e in self.edges:
            self.edges.remove(e)
            self.neighbors[u].remove(v)
            self.neighbors[v].remove(u)
            return True
        return False

    def rm_vertex(self, u):
        if u in self.neighbors:
            to_delete = list(self.neighbors[u])
            for v in to_delete:
                self.rm_edge(u, v)
            del self.neighbors[u]
            return True
        return False

    def degree(self, v):
        return len(self.neighbors[v])

    @property
    def m(self):
        # Return the number of edges
        return len(self.edges)

    @property
    def n(self):
        # Return the number of vertices
        return len(self.neighbors)


class Edge:
    def __init__(self, u, v, weight=0):
        if u == v:
            raise ValueError('Vertices for Edge must be distinct!')
        self.u = u
        self.v = v
        self.weight = weight

