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
        """Adds a vertex to the graph.

        :param v: The vertex to add.
        :return: Returns True if it succeeded, but if the vertex already exists we abort the add and return False.
        """
        """ """
        if v not in self.neighbors:
            self.neighbors[v] = set()
            return True
        return False

    def has_edge(self, u, v):
        """ Checks if the graph has the given edge between verticies u and v.

        :param u: The first vertex
        :param v: The second vertex
        :return: True if an edge exists between verticies v and v, otherwise False.
        """
        e = frozenset([u, v])
        return e in self.edges

    def add_edge(self, u, v):
        """Adds an edge between the two verticies u and v. Both verticies must exists first.

        :param u: The first vertex
        :param v: The second vertex
        :return: True if the operation succeeded, False otherwise.
        """
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
        """ Removes an edge between verticies u and v from the graph

        :param u: The first vertex
        :param v: The second vertex
        :return: True if the operation succeeded, False otherwise.
        """
        if self.has_edge(u, v):
            self.edges.remove(frozenset([u, v]))
            self.neighbors[u].remove(v)
            self.neighbors[v].remove(u)
            return True
        return False

    def rm_vertex(self, u):
        """ Removes a vertex (and any related edges) from the graph

        :param u: The vertex to remove.
        :return: True if the operation succeeded, false otherwise.
        """
        if u in self.neighbors:
            to_delete = list(self.neighbors[u])
            for v in to_delete:
                self.rm_edge(u, v)
            del self.neighbors[u]
            return True
        return False

    def degree(self, v):
        """Returns the number of neighbors a vertex has."""
        return len(self.neighbors[v])

    @property
    def m(self):
        """ Return the number of edges the graph contains."""
        return len(self.edges)

    @property
    def n(self):
        """Return the number of vertices the graph contains."""
        return len(self.neighbors)

    def connected(self, u, v):
        """Returns True if the two verticies are connected, otherwise False."""
        return v in self.dfs(u)

    def path(self, u, v):
        """Generates a path between verticies u and v using the depth first search tree.

        :param u: The starting vertex
        :param v: The ending vertex
        :return: A list of verticies to get from u to v.
        """

        tree = self.dfs(v)
        if u in tree:
            _path = []
            while u is not None:
                _path.append(u)
                u = tree[u]
            return _path

    def dfs(self, v):
        """Generates a depth first search tree for the graph from vertex v."""
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
        """Generates a bredth first search tree for the graph from vertex v."""

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
