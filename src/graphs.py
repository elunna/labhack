class Graph:
    """ Undirected graph: Implemented using an adjacency list
        edges: A set of frozen sets of 2 connected vertices.
        neighbors: A dict of Vertices as keys and sets of neighbors as values.
    """
    def __init__(self, vertices={}, edges={}):
        self.edges = set(frozenset((u, v)) for u, v in edges)
        self.neighbors = {}  # Change to defaultdict for sets

        for v in vertices:
            self.add_vertex(v)

        for u, v in self.edges:
            self.add_edge(u, v)

    def add_vertex(self, v):
        if v not in self.neighbors:
            self.neighbors[v] = set()

    def add_edge(self, u, v):
        self.edges.add(frozenset([u, v]))
        self.add_vertex(u)
        self.add_vertex(v)
        self.neighbors[u].add(v)
        self.neighbors[v].add(u)

    def rm_edge(self, u, v):
        e = frozenset([u, v])
        if e in self.edges:
            self.edges.remove()
            self.neighbors[u].remove(v)
            self.neighbors[v].remove(u)

    def rm_vertex(self, u):
        to_delete = list(self.neighbors[u])
        for v in to_delete:
            self.rm_edge(u, v)
        del self.neighbors[u]

    def degree(self, v):
        return len(self.neighbors[v])

    @property
    def m(self):
        # Return the number of edges
        return len(self.edges)

    def n(self):
        # Return the number of vertices
        return len(self.neighbors)