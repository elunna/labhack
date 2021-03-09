from collections import deque


class DirectedGraph:
    """A weighted and directed Graph."""
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
        return len(self.vertices) == 0

    @property
    def m(self):
        """ Gets the number of edges in the graph.

        :return:  the number of edges in the graph
        """
        return self.edge_count

    @property
    def n(self):
        """ Gets the number of vertices in the graph.

        :return: the number of vertices in the graph
        """
        return len(self.vertices)

    def clear(self):
        """ Removes all vertices and edges from the graph.

        :return: None
        """
        self.vertices.clear()
        self.edge_count = 0

    def reset_vertices(self):
        for v in self.vertices.values():
            v.visited = False
            v.set_cost(0)
            v.set_predecessor(None)

    def bft(self, origin):
        """ Performs a breadth-first traversal of a graph.

        :param origin: origin an object that labels the origin vertex of the traversal
        :return: a list of labels of the vertices in the traversal, with
        the label of the origin vertex at the queue's front
         """
        # Make sure all vertices are reset first
        self.reset_vertices()

        traversalOrder = deque()  # Queue
        vertexQueue = deque()  # Queue

        originVertex = self.vertices.get(origin)
        originVertex.visited = True
        traversalOrder.append(origin)  # enqueue vertex label
        vertexQueue.append(originVertex)  # enqueue vertex

        while vertexQueue:
            frontVertex = vertexQueue.popleft()

            for e in frontVertex.edgelist:
                nextNeighbor = e.vertex

                if not nextNeighbor.visited:
                    nextNeighbor.visited = True
                    traversalOrder.append(nextNeighbor.label)
                    vertexQueue.append(nextNeighbor)

        return list(traversalOrder)

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

    def shortest_path(self, begin, end):
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
        self.reset_vertices()
        done = False
        vertexQueue = deque()  # Queue for vertices
        originVertex = self.vertices.get(begin)
        endVertex = self.vertices.get(end)
        originVertex.visited = True
        path = []
        # Assertion: resetVertices() has executed setCost(0)
        # and setPredecessor(null) for originVertex

        vertexQueue.append(originVertex)

        while not done and vertexQueue:
            frontVertex = vertexQueue.popleft()

            for e in frontVertex.edgelist:
                nextNeighbor = e.vertex
                if nextNeighbor.visited is False:

                    nextNeighbor.visited = True
                    nextNeighbor.set_cost(1 + frontVertex.get_cost())
                    nextNeighbor.set_predecessor(frontVertex)
                    vertexQueue.append(nextNeighbor)

                if nextNeighbor == endVertex:
                    done = True

        # traversal ends; construct shortest path
        pathLength = int(endVertex.get_cost())
        path.append(endVertex.label)
        vertex = endVertex

        while vertex.has_predecessor():
            vertex = vertex.get_predecessor()
            path.append(vertex.label)

        return pathLength

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
        self.cost += new_cost

    def get_cost(self):
        """ Gets the recorded cost of the path to this vertex.
        :return: the cost of the path
        """
        return self.cost


class Edge:
    def __init__(self, end_vertex, weight):
        self.vertex = end_vertex
        self.weight = weight