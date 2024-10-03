import numpy as np
from scipy.sparse import lil_matrix
import time
from typing import List

class KProds:
    def __init__(self,  k: int, filePath: str) -> None:
        self.k = k # The number of matrices in Kronecker products
        ############## #TODO: Complete the function ##################
        # Initializes the KProds class.
        #
        # Args:
        #     k (int): The number of matrices in Kronecker products.
        #     filePath (str): Path to the file containing the initial matrix.
        #
        # This function loads the initial matrix from the specified file, and sets up class variables.
        ########################################################################
        initial_matrix = np.array([])
        with open(filePath) as f:
            for line in f:
                line = line.strip()
                numbers_strings = line.split("\t")
                numbers = [int(number) for number in numbers_strings]
                if initial_matrix.size == 0:
                    initial_matrix = np.append(initial_matrix, numbers)
                else:
                    initial_matrix = np.vstack((initial_matrix, numbers))

        self.initMat = initial_matrix

        self.N = self.initMat.shape[0]  # the size of initMat
        self.adj_list = [lil_matrix((self.N ** _k, self.N ** _k), dtype=np.int64) for _k in range(1, self.k+1)]
        ######################### Implementation end ###########################

    def produceGraph(self) -> List[lil_matrix]:
        ############## #TODO: Complete the function ############################
        # Computes the Kronecker powers of the initial matrix and generates a list of adjacency matrices.
        #
        # Returns:
        #     list of lil_matrix: A list of adjacency matrices representing Kronecker graphs 
        #     from 1 to k.
        #
        # This function calculates the k-th Kronecker power of the initial matrix using non-zero elements 
        # and stores the results in adjacency lists for each power level by calling the computeProb function.
        ########################################################################
        for row_idx in range(self.initMat.shape[0]):
            for col_idx in range(self.initMat.shape[1]):
                prod = self.initMat[row_idx, col_idx]
                self.computeProb(row_idx, col_idx, prod, 1)

        return self.adj_list

        ######################### Implementation end ###########################

    def computeProb(self, rowIdx, colIdx, prod, currk) -> None:
        ############## #TODO: Complete the function ############################
        # Recursively computes the Kronecker power of the initial matrix and updates adjacency lists.
        #
        # Args:
        #     rowIdx (int): Current row index in the Kronecker power matrix.
        #     colIdx (int): Current column index in the Kronecker power matrix.
        #     prod (float): The accumulated product value at the current index.
        #     currk (int): The current level of the Kronecker power.
        #
        # This method updates the adjacency matrix at the current level with the calculated probability 
        # and recursively computes the next level of the Kronecker power by multiplying the current 
        # product value with the non-zero elements of the initial matrix. The recursion stops 
        # when the maximum power level (self.k) is reached.
        ########################################################################
        if prod == 0:
            return
        if currk - 1 == self.k:
            return
        self.adj_list[currk - 1][rowIdx, colIdx] = prod

        for row_idx in range(self.initMat.shape[0]):
            for col_idx in range(self.initMat.shape[1]):
                self.computeProb(
                    row_idx + rowIdx * 4,
                    col_idx + colIdx * 4,
                    self.initMat[row_idx, col_idx],
                    currk + 1,
                )
        ######################### Implementation end ###########################
