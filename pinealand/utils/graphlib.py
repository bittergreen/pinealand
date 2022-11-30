from functools import wraps
import numpy as np


# read data from file
def read_data(data_path, weight_column_index, separator=','):
    out_edges = []
    in_edges = []
    if weight_column_index == 0:
        with open(data_path, 'r') as f:
            for row in f:
                temp = []
                temp_reverse = []
                temp.append(row.split(separator)[0])
                temp.append(row.split(separator)[1])
                temp_reverse.append(row.split(separator)[1])
                temp_reverse.append(row.split(separator)[0])
                out_edges.append(temp)
                in_edges.append(temp_reverse)
    else:
        with open(data_path, 'r') as f:
            for row in f:
                temp = []
                temp_reverse = []
                temp.append(row.split(separator)[0])
                temp.append(row.split(separator)[1])
                temp.append(row.split(separator)[weight_column_index - 1])
                temp_reverse.append(row.split(separator)[1])
                temp_reverse.append(row.split(separator)[0])
                temp_reverse.append(row.split(separator)[weight_column_index - 1])
                out_edges.append(temp)
                in_edges.append(temp_reverse)
    print("Data loaded successfully from file.")
    return out_edges, in_edges


# sorting in_edges & out_edges
# converting the ids to int for sorting
# converting the ids back to str afterwards
def sort_edges(data, weighted=False):
    if weighted:
        for i, row in enumerate(data):
            data[i] = list(map(int, row[0:2]))
            if len(row) == 3:
                data[i].append(float(row[2]))
        data.sort()
        for i, row in enumerate(data):
            data[i] = [str(row[0]), str(row[1]), row[2]]
    else:
        for i, row in enumerate(data):
            data[i] = list(map(int, row))
        data.sort()
        for i, row in enumerate(data):
            data[i] = list(map(str, row))
    return data


# create adjacency list for Graph object
# edge_list shall be like [[1,2], [1,3]] etc..
# id_mappers are for id mapping.....
def build_adjacency_list(edge_list, weighted=False, src_id_mapper=lambda x: x, dst_id_mapper=lambda x: x):
    adj = {}
    out_degree = {}
    in_degree = {}
    if weighted:
        for i, edge in enumerate(edge_list):
            a = src_id_mapper(edge[0])
            b = dst_id_mapper(edge[1])
            b_with_weight = (b, edge[2])
            if a not in adj:
                adj[a] = []
            if b not in adj:
                adj[b] = []
            if a not in out_degree:
                out_degree[a] = 0
            if b not in out_degree:
                out_degree[b] = 0
            if a not in in_degree:
                in_degree[a] = 0
            if b not in in_degree:
                in_degree[b] = 0
            if b not in adj[a]:
                adj[a].append(b_with_weight)
                out_degree[a] += 1
                in_degree[b] += 1
    else:
        for i, edge in enumerate(edge_list):
            a = src_id_mapper(edge[0])
            b = dst_id_mapper(edge[1])
            if a not in adj:
                adj[a] = []
            if b not in adj:
                adj[b] = []
            if a not in out_degree:
                out_degree[a] = 0
            if b not in out_degree:
                out_degree[b] = 0
            if a not in in_degree:
                in_degree[a] = 0
            if b not in in_degree:
                in_degree[b] = 0
            if b not in adj[a]:
                adj[a].append(b)
                out_degree[a] += 1
                in_degree[b] += 1
    print("Constructed the adjacency list, out_degree & in_degree dict for the graph.")
    return adj, out_degree, in_degree


class Vertex(object):

    def __init__(self, vid, out_degree, in_degree, out_weight_sum=0.0, in_weight_sum=0.0):
        self.vid = vid
        self.out_degree = out_degree
        self.in_degree = in_degree
        self.out_weight_sum = out_weight_sum
        self.in_weight_sum = in_weight_sum


class Graph(object):

    def __init__(self, in_list, weighted=False, src_id_mapper=lambda x: x, dst_id_mapper=lambda x: x):
        self.weighted = weighted
        self.__adj_list, self.__out_degree, self.__in_degree = \
            build_adjacency_list(in_list, weighted, src_id_mapper, dst_id_mapper)
        self.__vertices = self.build_vertices()
        self.vn = len(self.__vertices)
        print("Graph constructed successfully.")

    def build_vertices(self):
        vertices = {}
        for vid in self.__adj_list.keys():
            edges = self.__adj_list[vid]
            if self.weighted:
                out_weight_sum = 0.0
                for edge in edges:
                    out_weight_sum += edge[1]
                vertex = Vertex(vid, self.__out_degree[vid], self.__in_degree[vid], out_weight_sum=out_weight_sum)
            else:
                vertex = Vertex(vid, self.__out_degree[vid], self.__in_degree[vid])
            vertices[vid] = vertex
        return vertices

    def get_vertices(self):
        return self.__vertices

    def get_adj_list(self):
        return self.__adj_list

    def get_out_degrees(self):
        return self.__out_degree

    def get_in_degrees(self):
        return self.__in_degree


def edge_traverse_algorithm(algo):
    """Decorator for all graph algorithms that work through edge traversing"""

    @wraps(algo)
    def execute(graph: Graph, *args):
        adj_list = graph.get_adj_list()
        vertices = graph.get_vertices()
        for src_id in adj_list.keys():
            dst_list = adj_list[src_id]
            if graph.weighted:
                for edge in dst_list:
                    dst_id = edge[0]
                    weight = edge[1]
                    # pass params to the algo
                    algo(src_id,
                         dst_id,
                         weight,
                         vertices,
                         args)
            else:
                for edge in dst_list:
                    dst_id = edge
                    weight = 1.0
                    # pass params to the algo
                    algo(src_id,
                         dst_id,
                         weight,
                         vertices,
                         args)

    return execute


@edge_traverse_algorithm
def _weighted_pagerank_traverse(src, dst, weight, vertices: {str: Vertex}, *args):
    curr_rank = args[0][0]
    next_rank = args[0][1]
    out_weight_sum = vertices[src].out_weight_sum
    change = 0.0
    if out_weight_sum != 0:
        change = curr_rank[int(src)-1] / out_weight_sum
    next_rank[int(dst)-1] += change


def weighted_pagerank(graph: Graph, damping=0.85, rounds=10):
    """PageRank algorithm realized through edge traversing on adjacency list representation of the Graph"""
    """Notice the np.array indices starts from 0, but our vertex id starts from 1"""
    vn = graph.vn
    curr_rank = np.ones(vn) / vn
    next_rank = np.zeros(vn)
    iteration = 0
    const = (1-damping) / vn

    # pagerank formula
    def pagerank_vertex_update(elem: float):
        return const + damping * elem

    while iteration < rounds:
        _weighted_pagerank_traverse(graph, curr_rank, next_rank)
        for x in np.nditer(next_rank, op_flags=['readwrite']):
            x[...] = pagerank_vertex_update(x)
        curr_rank = next_rank
        next_rank = np.zeros(vn)
        iteration += 1
        print("Pagerank round %s finished!" % iteration)

    return curr_rank


@edge_traverse_algorithm
def _hits_traverse(src, dst, weight, vertices: {str: Vertex}, *args):
    curr_auth = args[0][0]
    next_auth = args[0][1]
    curr_hub = args[0][2]
    next_hub = args[0][3]
    next_auth[int(dst)-1] += curr_hub[int(src)-1]
    next_hub[int(src)-1] += curr_auth[int(dst)-1]


def hits(graph: Graph, rounds=10):
    """PageRank algorithm realized through edge traversing on adjacency list representation of the Graph"""
    """Notice the np.array indices starts from 0, but our vertex id starts from 1"""
    vn = graph.vn
    curr_auth = np.ones(vn) / vn
    next_auth = np.ones(vn) / vn
    curr_hub = np.ones(vn) / vn
    next_hub = np.ones(vn) / vn
    iteration = 0

    while iteration < rounds:
        _hits_traverse(graph, curr_auth, next_auth, curr_hub, next_hub)
        curr_auth = next_auth
        curr_hub = next_hub
        next_auth = np.zeros(vn)
        next_hub = np.zeros(vn)
        iteration += 1
        print("HITS round %s finished!" % iteration)

    return curr_auth, curr_hub

