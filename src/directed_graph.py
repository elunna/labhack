from src.vertex import Vertex


class DirectedGraph:
    # TODO: Implement contains for vertices
    # TODO: Add add_vertices
    # TODO: Add add_edges
    # TODO: Let us init with vertices
    # TODO: Let us init with edges

    def __init__(self):
        self.vertices = {}
        self.edge_count = 0

    def add_vertex(self, vertex_label):
        """ Adds a given vertex to the graph.

        :param vertex_label: an object that labels the new vertex and is
        distinct from the labels of current vertices
        :return: True if the vertex is added, or False if not
        """
        if vertex_label in self.vertices:
            return False
        self.vertices[vertex_label] = Vertex(vertex_label)
        return True

    def add_edge(self, begin, end, weight=0):
        """ Adds a weighted edge between two given distinct vertices that
        are currently in the graph. The desired edge must not already
        be in the graph. In a directed graph, the edge points toward
        the second vertex given.

        :param begin: begin an object that labels the origin vertex of the edge
        :param end: end an object, distinct from begin, that labels the end
        # vertex of the edge
        :param weight: the real value of the edge's weight
        :return: True if the edge is added, or False if not
        """
        begin_vertex = self.vertices.get(begin)
        end_vertex = self.vertices.get(end)

        result = False
        if begin_vertex and end_vertex:
            result = begin_vertex.connect(end_vertex, weight)
        if result:
            self.edge_count += 1

        return result

    def has_edge(self, begin, end):
        """ Sees whether an edge exists between two given vertices.

        :param begin: begin an object that labels the origin vertex of the edge
        :param end: an object that labels the end vertex of the edge
        :return: True if an edge exists
        """
        beginVertex = self.vertices.get(begin)
        endVertex = self.vertices.get(end)

        if beginVertex and endVertex:
            for e in beginVertex.edgelist:
                next_neighbor = e.vertex

                if endVertex == next_neighbor:
                    return True

        return False

    def is_empty(self):
        """ Sees whether the graph is empty.

        :return: True if the graph is empty
        """
        pass

    def get_number_of_vertices(self):
        """ Gets the number of vertices in the graph.

        :return: the number of vertices in the graph
        """
        pass

    def get_number_of_edges(self):
        """ Gets the number of edges in the graph.

        :return:  the number of edges in the graph
        """
        pass

    def clear(self):
        """ Removes all vertices and edges from the graph.

        :return: None
        """
        pass

    def get_breadth_first_traversal(self, origin):
        """ Performs a breadth-first traversal of a graph.

        :param origin: origin an object that labels the origin vertex of the traversal
        :return: a queue of labels of the vertices in the traversal, with
        the label of the origin vertex at the queue's front
        """
        pass

    def get_depth_first_traversal(self, origin):
        """ Performs a depth-first traversal of a graph.

        :param origin: origin an object that labels the origin vertex of the traversal
        :return:  a queue of labels of the vertices in the traversal, with
        the label of the origin vertex at the queue's front
        """
        pass

    def get_topological_order(self):
        """ Performs a topological sort of the vertices in a graph without cycles.

        :return: a stack of vertex labels in topological order, beginning
        with the stack's top
        """
        pass

    def get_shortest_path(self, begin, end, path):
        """ Finds the path between two given vertices that has the shortest length.

        :param begin: begin an object that labels the path's origin vertex
        :param end: end an object that labels the path's destination vertex
        :param path: path a stack of labels that is empty initially;
            at the completion of the method, this stack contains
            the labels of the vertices along the shortest path;
            the label of the origin vertex is at the top, and
            the label of the destination vertex is at the bottom
        :return: the length of the shortest path
        """
        pass

    def get_cheapest_path(self, begin, end, path):
        """ Finds the least-cost path between two given vertices.

        :param begin: begin an object that labels the path's origin vertex
        :param end: end an object that labels the path's destination vertex
        :param path: path a stack of labels that is empty initially;
            at the completion of the method, this stack contains
            the labels of the vertices along the cheapest path;
            the label of the origin vertex is at the top, and
            the label of the destination vertex is at the bottom
        :return: the cost of the cheapest path
        """
    pass
