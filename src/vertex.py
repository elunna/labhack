class Vertex(object):
    def get_label(self):
        """ Gets the vertex's label.

        :return: the object that labels the vertex
        """
        raise NotImplementedError()

    def visit(self):
        """ Marks the vertex as visited.

        :return:  None
        """
        raise NotImplementedError()

    def unvisit(self):
        """ Removes the vertex's visited mark.

        :return:  None
        """
        raise NotImplementedError()

    def is_visited(self):
        """ Sees whether the vertex is marked as visited.

        :return:  true if the vertex is visited
        """
        raise NotImplementedError()

    def connect(self, end_vertex, edge_weight):
        """ Connects this vertex and a given vertex with a weighted edge. The two vertices cannot be the same, and must
        not already have this edge between them. In a directed graph, the edge points toward the given vertex.

        :param end_vertex: a vertex in the graph that ends the edge
        :param edge_weight: a real-valued edge weight, if any
        :return: true if the edge is added, or false if not
        """
        raise NotImplementedError()

    def get_neighbor_iterator(self):
        """ Creates an iterator of this vertex's neighbors by following all edges that begin at this vertex.

        :return: an iterator of the neighboring vertices of this vertex
        """
        raise NotImplementedError()

    def get_weight_iterator(self):
        """ Creates an iterator of the weights of the edges to this vertex's neighbors.

        :return: an iterator of edge weights for edges to neighbors of this vertex
        """
        raise NotImplementedError()

    def has_neighbor(self):
        """ Sees whether this vertex has at least one neighbor.

        :return: true if the vertex has a neighbor
        """
        raise NotImplementedError()

    def get_unvisited_neighbor(self):
        """ Gets an unvisited neighbor, if any, of this vertex.

        :return: either a vertex that is an unvisited neighbor or null if no such neighbor exists
        """
        raise NotImplementedError()

    def set_predecessor(self, predecessor):
        """ Records the previous vertex on a path to this vertex.

        :param predecessor: predecessor the vertex previous to this one along a path
        :return:  None
        """
        raise NotImplementedError()

    def get_predecessor(self):
        """  Gets the recorded predecessor of this vertex.

        :return: either this vertex's predecessor or null if no predecessor was recorded
        """
        raise NotImplementedError()

    def has_predecessor(self):
        """ Sees whether a predecessor was recorded.

        :return: true if a predecessor was recorded for this vertex
        """
        raise NotImplementedError()

    def set_cost(self, new_cost):
        """ Records the cost of a path to this vertex.

        :param new_cost: newCost the cost of the path
        :return:
        """
        raise NotImplementedError()

    def get_cost(self):
        """ Gets the recorded cost of the path to this vertex.

        :return: the cost of the path
        """
        raise NotImplementedError()