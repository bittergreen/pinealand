from pinealand.utils import graphlib
import numpy as np

data_path = '/home/wengqi/dataset/ml-100k/u.data'
separator = '\t'
weight_column_index = 3

out_edges, in_edges = graphlib.read_data(data_path, weight_column_index, separator)

"""out_edges按起点排序，每条边数据第一个元素是起点；in_edges按终点排序，每条边数据第一个元素是终点(只用了out_edges)"""
out_edges = graphlib.sort_edges(out_edges, weighted=True)
in_edges = graphlib.sort_edges(in_edges, weighted=True)

"""
这个数据集很搞，userid和movie id都是从0开始排的，需要做一下id-mapping
943 users on 1682 items
items(movie id)改到944开始，944-2625  lambda x: str(int(x)+943)
"""
graph = graphlib.Graph(out_edges, weighted=True, dst_id_mapper=lambda x: str(int(x) + 943))

rank = graphlib.weighted_pagerank(graph, rounds=10)

auth, hub = graphlib.hits(graph, rounds=10)

user_rank = rank[:943]
movie_rank = rank[943:2625]
user_auth = auth[:943]
movie_auth = auth[943:2625]
user_hub = hub[:943]
movie_hub = hub[943:2625]

top_movies = np.argsort(movie_rank)


def naive_read_file(path):
    item_list = []
    with open(path) as f:
        for row in f:
            item_list.append(row)
    return item_list


movie_path = '/home/wengqi/dataset/ml-100k/u.item'
user_path = '/home/wengqi/dataset/ml-100k/u.user'

movie_info = naive_read_file(movie_path)
user_info = naive_read_file(user_path)

iter = 10
for index in np.nditer(top_movies[-10:]):
    tmp_rank = movie_rank[index]
    tmp_info = movie_info[index]
    print("Rank %s is movie %s" % (iter, tmp_info))
    print("with pagerank value of %s" % tmp_rank)
    print(" ")
    print("______________________________________________________")
    iter -= 1

