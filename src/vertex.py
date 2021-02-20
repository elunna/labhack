class Vertex:
    def __init__(self):
        pass

    def connect(self, end_vertex, edge_weight):
        """ Connects this vertex and a given vertex with a weighted edge.
        The two vertices cannot be the same, and must not already
        have this edge between them. In a directed graph, the edge
        points toward the given vertex.

        :param end_vertex: a vertex in the graph that ends the edge
        :param edge_weight: a real-valued edge weight, if any
        :return: True if the edge is added, or False if not
        """
        pass

    def get_neighbor_iter(self):
        """ Creates an iterator of this vertex's neighbors by following
        all edges that begin at this vertex.

        :return: an iterator of the neighboring vertices of this vertex
        """
        pass

    def get_weight_iter(self):
        """ Creates an iterator of the weights of the edges to this vertex's neighbors.

        :return: an iterator of edge weights for edges to neighbors of this vertex
        """
        pass

    def has_neighbor(self):
        """ Sees whether this vertex has at least one neighbor.

        :return: True if the vertex has a neighbor, False otherwise.
        """
        pass

    def get_unvisited_neighbor(self):
        """ Gets an unvisited neighbor, if any, of this vertex.

        :return: either a vertex that is an unvisited neighbor or None
        if no such neighbor exists
        """
        pass

    def set_predecessor(self, predecessor):
        """ Records the previous vertex on a path to this vertex.

        :param predecessor: the vertex previous to this one along a path
        :return:
        """
        pass

    def get_predecessor(self):
        """ Gets the recorded predecessor of this vertex.

        :return: either this vertex's predecessor or None if no predecessor was recorded
        """
        pass

    def has_predecessor(self):
        """ Sees whether a predecessor was recorded.

        :return: True if a predecessor was recorded for this vertex
        """
        pass

    def set_cost(self, new_cost):
        """ Records the cost of a path to this vertex.

        :param new_cost: the cost of the path
        :return: None
        """
        pass

    def get_cost(self):
        """ Gets the recorded cost of the path to this vertex.
        :return: the cost of the path
        """
        pass
