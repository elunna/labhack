class Graph:
    """ An interface of methods providing basic operations for directed
    and undirected graphs that are either weighted or unweighted.
    """

    def add_vertex(self, name) -> bool:
        """ Adds a given vertex to the graph.

        :param name: labels the new vertex and is distinct from the labels of current vertices
        :return: true if the vertex is added, or false if not
        """

    def add_edge(self, begin, end, weight) -> bool:
        """ Adds a weighted edge between two given distinct vertices that
            are currently in the graph. If no weight is supplied, the weight defaults to 0.
            The desired edge must not already be in the graph. In a directed graph, the edge
            points toward the second vertex given.

        :param begin: begin an object that labels the origin vertex of the edge
        :param end: end an object, distinct from begin, that labels the end
            vertex of the edge
        :param weight: the real value of the edge's weight
        :return: true if the edge is added, or false if not
        """

    def has_edge(self, begin, end) -> bool:
        """ Sees whether an edge exists between two given vertices.

        :param begin: an object that labels the origin vertex of the edge
        :param end: an object that labels the end vertex of the edge
        :return: if an edge exists
        """

    def is_empty(self) -> bool:
        """ Sees whether the graph is empty.

        :return: true if the graph is empty
        """

    def m(self) -> int:
        """ Gets the number of vertices in the graph.
        :return: the number of vertices in the graph
        """

    def n(self) -> int:
        """ Gets the number of edges in the graph.
        :return:  the number of edges in the graph
        """

    def clear(self) -> None:
        """ Removes all vertices and edges from the graph.
        """

