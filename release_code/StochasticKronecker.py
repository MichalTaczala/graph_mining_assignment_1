import numpy as np
from scipy.sparse import lil_matrix
import time
from typing import List
from typing import Tuple

class STKProds:
    def __init__(self,  k: int, real_adj: lil_matrix, filePath: str) -> None:
        self.k = k # The number of matrices in Kronecker products
        ############## #TODO: Complete the function #################################
        # Initializes the STKProds class.
        #
        # Args:
        #     k (int): The number of matrices in Kronecker products
        #     real_adj (lil_matrix): The real-world adjacency matrix used to set target edge counts.
        #     filePath (str): Path to the file containing the initial matrix.
        #
        # This method loads the initial matrix from the specified file, sets up the class variables, 
        # calculates the target edge number of each Kronecker power level from the real-world adjacency matrix
        # and initializes adjacency lists for storing the Kronecker product graphs.
        ############################################################################

        # initialize base matrix
        initial_matrix = np.array([])
        with open(filePath) as f:
            for line in f:
                line = line.strip()
                numbers_strings = line.split("   ")
                numbers = [float(number) for number in numbers_strings]
                if initial_matrix.size == 0:
                    initial_matrix = np.append(initial_matrix, numbers)
                else:
                    initial_matrix = np.vstack((initial_matrix, numbers))

        self.initMat = initial_matrix

        self.N = self.initMat.shape[0]
        size_list = [self.N **_k for _k in range(1, self.k)] + [real_adj.shape[0]]
        self.real_edgenum_list = [np.sum(real_adj[:_size, :_size] ) for _size in size_list]
        self.adj_list = [lil_matrix((self.N ** _k, self.N ** _k), dtype=np.int64) for _k in range(1, self.k+1)]
        ######################### Implementation end ###########################

    def produceGraph(self) -> List[lil_matrix]:
        ############## #TODO: Complete the function #################################
        # Generates Kronecker graphs based on the specified number of edges at each power level.
        #
        # Returns:
        #     list of lil_matrix: A list of adjacency matrices representing Kronecker graphs from 1 to k.
        #
        # This method iterates through each Kronecker power level and generates edges by calling the computeProb function until the target edge number is reached, as estimated from the real-world graph.
        ############################################################################

        sum_of_probabilities = self.initMat.sum()
        self.initMat2 = self.initMat / sum_of_probabilities
        nr_rows, nr_cols = self.initMat.shape
        self.indexes = [(row, col) for row in range(nr_rows) for col in range(nr_cols)]
        self.flattened = self.initMat2.flatten().tolist()
        for power_level in range(1, self.k + 1):
            current_number_of_edges = 0
            limit = self.real_edgenum_list[power_level - 1]
            while current_number_of_edges < limit:
                row, col = self.computeProb(power_level)
                if self.adj_list[power_level - 1][row, col] != 1:
                    current_number_of_edges += 1
                    self.adj_list[power_level - 1][row, col] = 1

        return self.adj_list

        ######################### Implementation end ###############################

    def computeProb(self, currk) -> Tuple[int, int]:
        ############## #TODO: Complete the function #################################
        # Samples the row and column indices for placing an edge in the Kronecker power matrix.
        #
        # Args:
        #     currk (int): The current level of the Kronecker power.
        #
        # Returns:
        #     tuple: The row and column indices where the edge is placed.
        #
        # This method generates indices based on the probability distribution derived 
        # from the initial matrix. It recursively samples indices at each level until 
        # the specified Kronecker power level is reached.
        ############################################################################
        if currk == 0:
            return (0, 0)

        chosen_option = int(np.random.choice(len(self.indexes), 1, p=self.flattened))
        non_recursive_part = np.array(self.indexes[chosen_option]) * 2 ** (currk - 1)
        recursive_part = self.computeProb(currk - 1)
        return tuple(
            first + second for first, second in zip(non_recursive_part, recursive_part)
        )
        ######################### Implementation end ###############################
