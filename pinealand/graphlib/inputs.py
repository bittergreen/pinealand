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
def sort_edge_list(data, weighted=False):
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
