from collections import deque


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

    def has_edge(self, u, v):
        e = frozenset([u, v])
        return e in self.edges

    def add_edge(self, u, v):
        # The vertices must exist for the edge to be formed
        if u not in self.neighbors or v not in self.neighbors:
            return False

        # The edge must not already exist in the graph.
        if not self.has_edge(u, v):
            self.edges.add(frozenset([u, v]))
            self.neighbors[u].add(v)
            self.neighbors[v].add(u)
            return True
        return False

    def rm_edge(self, u, v):
        if self.has_edge(u, v):
            self.edges.remove(frozenset([u, v]))
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

    def connected(self, u, v):
        # Are these two vertices connected?
        return v in self.dfs(u)

    def path(self, u, v):
        tree = self.dfs(v)
        if u in tree:
            _path = []
            while u is not None:
                _path.append(u)
                u = tree[u]
            return _path

    def dfs(self, v):
        # dict for rooted tree that matches vertices to their parents.
        tree = {}

        # Stack for visiting edges.
        # We will start with a fake Edge to start at v (first edge to visit)
        tovisit = [(None, v)]

        # To find a path to v, we can follow it's parents all the way up.
        while tovisit:
            a, b = tovisit.pop()

            if b not in tree:
                tree[b] = a

                for c in self.neighbors[b]:
                    tovisit.append((b, c))

        return tree

    def bfs(self, v):
        tree = {}
        # We will use a queue (the deque serves as a queue here) so we always search the closest neighbors first.
        tovisit = deque()
        tovisit.append((None, v))

        while tovisit:
            a, b = tovisit.popleft()
            if b not in tree:
                tree[b] = a

                for c in self.neighbors[b]:
                    tovisit.append((b, c))
        return tree
