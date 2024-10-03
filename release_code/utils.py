import numpy as np
from scipy.sparse import lil_matrix
import time
import datetime
import os

def read_graph(graph_fname):
    
    if os.path.isfile(graph_fname + ".txt"):
        with open(graph_fname + ".txt") as f:
            lines = f.read().split("\n")
            for line in lines:
                if not line: continue
                if line.startswith("number of nodes"):
                    num_nodes = int(line.split(": ")[-1])
                    adj_real = lil_matrix((num_nodes, num_nodes), dtype=np.int64)
                else:
                    words = line.split("\t")
                    node1, node2 = int(words[0]), int(words[1])
                    adj_real[node1, node2] = 1
                    adj_real[node2, node1] = 1
    else:
        print("There is no existing real-world graph file")
        adj_real = None
            
    return adj_real 