from pinealand.graphlib.elements import *

from functools import wraps
import numpy as np


# Todo: make this a decorator class inherited from class Algorithm
def edge_traverse_algorithm(algo):
    """Decorator for all graph algorithms that work through edge traversing"""

    @wraps(algo)
    def execute(graph: Graph, *args):
        adj_list = graph.get_adj_list()
        for src_vertex in adj_list.keys():
            dst_list = adj_list[src_vertex]
            for edge in dst_list:
                # pass params to the algo
                algo(edge, args)

    return execute


@edge_traverse_algorithm
def _pagerank_traverse(edge: Edge, *args):
    src_vertex, dst_vertex, weight = edge.src, edge.dst, edge.weight
    curr_rank = args[0][0]
    next_rank = args[0][1]
    out_weight_sum = src_vertex.get_out_weight_sum()
    change = 0.0
    if out_weight_sum != 0:
        change = curr_rank[int(src_vertex.vid)-1] * weight / out_weight_sum
    next_rank[int(dst_vertex.vid)-1] += change


def pagerank(graph: Graph, damping=0.85, rounds=10):
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
        _pagerank_traverse(graph, curr_rank, next_rank)
        for x in np.nditer(next_rank, op_flags=['readwrite']):
            x[...] = pagerank_vertex_update(x)
        curr_rank = next_rank
        next_rank = np.zeros(vn)
        iteration += 1
        print("Pagerank round %s finished!" % iteration)

    return curr_rank


@edge_traverse_algorithm
def _hits_traverse(edge: Edge, *args):
    src_vertex, dst_vertex, weight = edge.src, edge.dst, edge.weight
    curr_auth = args[0][0]
    next_auth = args[0][1]
    curr_hub = args[0][2]
    next_hub = args[0][3]
    next_auth[int(dst_vertex.vid)-1] += curr_hub[int(src_vertex.vid)-1]
    next_hub[int(src_vertex.vid)-1] += curr_auth[int(dst_vertex.vid)-1]


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
        # normalization
        auth_sum = curr_auth.sum()
        hub_sum = curr_hub.sum()
        curr_auth /= auth_sum
        curr_hub /= hub_sum
        iteration += 1
        print("HITS round %s finished!" % iteration)

    return curr_auth, curr_hub
