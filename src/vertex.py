from src.edge import Edge

# TODO: Implement equals?
# TODO: get_weight_iter?
# TODO: neighbors iterator


class Vertex:
    def __init__(self, label):
        self.label = label
        self.edgelist = []  # edges to neighbors
        self.visited = False  # True if visited
        self.prev_vertex = None  # on path to this vertex
        self.cost = 0  # of path to this vertex
        self.predecessor = None

    def connect(self, end_vertex, edge_weight=0):
        """ Connects this vertex and a given vertex with a weighted edge. The two vertices cannot be
        the same, and must not already have this edge between them. In a directed graph, the edge
        points toward the given vertex.

        :param end_vertex: a vertex in the graph that ends the edge
        :param edge_weight: a real-valued edge weight, if any
        :return: True if the edge is added, or False if not
        """
        result = False
        if end_vertex != self:
            # vertices are distinct
            duplicateEdge = False

            for e in self.edgelist:
                next_neighbor = e.vertex
                if end_vertex == next_neighbor:
                    duplicateEdge = True
                    break

            if not duplicateEdge:
                # Create a new Edge between the 2 verticies.
                self.edgelist.append(
                    Edge(end_vertex, edge_weight)
                )
                result = True

        return result

    def get_weight_iter(self):
        """ Creates an iterator of the weights of the edges to this vertex's neighbors.

        :return: an iterator of edge weights for edges to neighbors of this vertex
        """
        pass

    def has_neighbor(self):
        """ Sees whether this vertex has at least one neighbor.

        :return: True if the vertex has a neighbor, False otherwise.
        """
        return len(self.edgelist) > 0

    def get_unvisited_neighbor(self):
        """ Gets an unvisited neighbor, if any, of this vertex.

        :return: either a vertex that is an unvisited neighbor or None
        if no such neighbor exists
        """
        for edge in self.edgelist:
            next_neighbor = edge.vertex
            if next_neighbor.visited is False:
                return next_neighbor
        return None

    def set_predecessor(self, predecessor):
        """ Records the previous vertex on a path to this vertex.

        :param predecessor: the vertex previous to this one along a path
        :return:
        """
        self.predecessor = predecessor

    def get_predecessor(self):
        """ Gets the recorded predecessor of this vertex.

        :return: either this vertex's predecessor or None if no predecessor was recorded
        """
        return self.predecessor

    def has_predecessor(self):
        """ Sees whether a predecessor was recorded.

        :return: True if a predecessor was recorded for this vertex
        """
        return self.predecessor is not None

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
