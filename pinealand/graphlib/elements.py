import abc

"""
Reform the Graph & GraphElements structures according to the Pregel model
@author: bittergreen
@date: 2023.01.19
"""


class GraphElement(object):

    def __init__(self, value):
        self._value = value

    def get_value(self):
        return self._value

    def mutable_value(self, new_value):
        self._value = new_value
        return self._value

    def compute(self):
        pass


class Vertex(object):

    def __init__(self, vid: int, out_degree=0, in_degree=0, out_weight_sum=0.0, in_weight_sum=0.0):
        self.vid = vid
        self.__out_degree = out_degree
        self.__in_degree = in_degree
        self.__out_weight_sum = out_weight_sum
        self.__in_weight_sum = in_weight_sum

    def get_out_degree(self):
        return self.__out_degree

    def get_in_degree(self):
        return self.__in_degree

    def set_out_degree(self, out_degree: int):
        self.__out_degree = out_degree

    def set_in_degree(self, in_degree: int):
        self.__in_degree = in_degree

    def get_out_weight_sum(self):
        return self.__out_weight_sum

    def get_in_weight_sum(self):
        return self.__in_weight_sum

    def set_out_weight_sum(self, weight_sum):
        self.__out_weight_sum = weight_sum
        return self.__out_weight_sum

    def set_in_weight_sum(self, weight_sum):
        self.__in_weight_sum = weight_sum
        return self.__in_weight_sum


class Edge(object):

    def __init__(self, src=None, dst=None, weight=None):
        self.src = src
        self.dst = dst
        self.weight = weight

    def set_src_node(self, src_node: Vertex):
        self.src = src_node

    def set_dst_node(self, dst_node: Vertex):
        self.dst = dst_node

    def update_weight(self, weight: float):
        self.weight = weight


class Graph(object):

    """
    Graph object that contains Vertex & Edge objects(or their children)
    __vertices: {vid: Vertex}
    __adj_list: {Vertex: [Edge]}
    """
    def __init__(self, weighted, edge_list=None, src_id_mapper=lambda x: x, dst_id_mapper=lambda x: x):
        self.weighted = weighted
        if edge_list is None:
            self.__vertices, self.__adj_list = {}, {}
        else:
            self.__vertices, self.__adj_list = \
                self.build_vertices_and_adjacency_list(edge_list, weighted, src_id_mapper, dst_id_mapper)
        self.vn = len(self.__vertices)
        self.update_vertices_out_weight_sum()
        print("Graph constructed successfully.")

    # create vertices and adjacency list for Graph object from an edge_list
    # edge_list shall be like [[1,2], [1,3]] etc..
    # id_mappers are for id mapping.....
    @staticmethod
    def build_vertices_and_adjacency_list(edge_list, weighted=False, src_id_mapper=lambda x: x, dst_id_mapper=lambda x: x):
        vertices = {}
        adj = {}
        for i, edge in enumerate(edge_list):
            id_va = src_id_mapper(edge[0])
            id_vb = dst_id_mapper(edge[1])
            if weighted:
                weight = edge[2]
            else:
                weight = 1.0
            if id_va not in vertices:
                va = Vertex(id_va)
                vertices[id_va] = va
            else:
                va = vertices[id_va]
            if id_vb not in vertices:
                vb = Vertex(id_vb)
                vertices[id_vb] = vb
            else:
                vb = vertices[id_vb]
            if va not in adj:
                adj[va] = []
            if vb not in adj:
                adj[vb] = []
            # update degrees
            va.set_out_degree(va.get_out_degree() + 1)
            vb.set_in_degree(vb.get_in_degree() + 1)
            edge_ab = Edge(va, vb, weight)
            # Todo: consider multi-graph processing
            if edge_ab not in adj[va]:
                adj[va].append(edge_ab)
        print("Successfully constructed the vertices & the adjacency list.")
        return vertices, adj

    def get_vertices(self):
        return self.__vertices

    def get_adj_list(self):
        return self.__adj_list

    def add_vertex(self, vid):
        """
        Add vertex through vid
        Todo: Add different ways of adding vertices!
        """
        vertex = Vertex(vid)
        self.__vertices[vid] = vertex
        return vertex

    def add_edge(self, edge_elem):
        """
        Todo: Add different ways of adding edges!
        Todo: check if edge already exists? Since edges have no indexes, there's no straightforward way to do this.
        :param edge_elem: (srcId, dstId, weight) / (srcId, dstId)
        """
        src_id = edge_elem[0]
        dst_id = edge_elem[1]
        if len(edge_elem) <= 2:
            weight = 1.0
        else:
            weight = edge_elem[2]
        if src_id not in self.__vertices:
            src_vertex = self.add_vertex(src_id)
        else:
            src_vertex = self.__vertices[src_id]
        if dst_id not in self.__vertices:
            dst_vertex = self.add_vertex(dst_id)
        else:
            dst_vertex = self.__vertices[dst_id]
        if src_vertex not in self.__adj_list:
            self.__adj_list[src_vertex] = []
        if dst_vertex not in self.__adj_list:
            self.__adj_list[dst_vertex] = []
        self.__adj_list[src_vertex].append(Edge(src_vertex, dst_vertex, weight))

    def update_vertices_out_weight_sum(self):
        """Compute and update the out_weight_sum of all vertices in the graph"""
        for src_vertex in self.__adj_list.keys():
            edges = self.__adj_list[src_vertex]
            if self.weighted:
                out_weight_sum = 0.0
                for edge in edges:
                    out_weight_sum += edge.weight
                src_vertex.set_out_weight_sum(out_weight_sum)
            else:
                src_vertex.set_out_weight_sum(float(src_vertex.get_out_degree()))
        return True

