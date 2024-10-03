import matplotlib.pyplot as plt
import numpy as np
import random
import datetime
from scipy.sparse.linalg import svds

class Analysis:
    def __init__(self, adj_list, real_adj, outputName) -> None:
        # Initializes the Analysis class.
        #
        # Args:
        #     adj_list (list of lil_matrix): List of adjacency matrices representing Kronecker graphs.
        #     real_adj (lil_matrix or None): Real-world adjacency matrix for comparison; None if not available.
        #     outputName (str): Name used for output files (e.g., plots).
        #
        # This method sets up the analysis by initializing variables, computing graph properties such as 
        # degree distribution, diameter, and density, and generates plots to compare the generated and real graphs.
        #####################################################################################3
        self.outputName = outputName
        
        self.adj_list = adj_list
        self.N = self.adj_list[0].shape[0]
        
        # Check if the real adjacency matrix is provided
        self.real_adj_exist_flag = False
        if real_adj is not None:
            self.real_adj_exist_flag = True
            size_list = [self.N**_k for _k in range(1, len(adj_list))] + [real_adj.shape[0]]
            self.real_adj_list = [real_adj[:_size, :_size] for _size in size_list]
        
        # Compute degree distribution, diameter, and density for the generated graphs
        self.degree_ours = self.computeDegDist(self.adj_list[-1])
        self.density = self.computeDenDist(self.adj_list)
        self.svs = self.computeSvDist(self.adj_list[-1])
        # If real graphs exist, compute their properties for comparison
        if self.real_adj_exist_flag:
            self.degree_reals = self.computeDegDist(self.real_adj_list[-1])
            self.density_real = self.computeDenDist(self.real_adj_list)
            self.svs_real = self.computeSvDist(self.real_adj_list[-1])
            
        # Plot comparisons between generated and real graphs
        self.plotDegDist()
        self.plotDenDist()
        self.plotSvDist()
        
    def computeDegDist(self, _adj):
        # Computes the degree distribution of the given adjacency matrix.
        _degrees = {}
        num_nodes = _adj.shape[0]
        for i in range(num_nodes):
            deg = _adj[i].getnnz()
            if deg not in _degrees:
                _degrees[deg] = 0
            _degrees[deg] += 1
        return _degrees        
        
    def computeDenDist(self, _adj_list):
        # Computes the edge density of each adjacency matrix in the list.
        _density = {}
        for i in range(len(_adj_list)):
            num_nodes = _adj_list[i].shape[0]
            _density[num_nodes] = np.sum(_adj_list[i])
        return _density
        
    def computeSvDist(self, _adj):
        # Computes the singular value distribution of the given adjacency matrix.
        _svs = {}
        _, sv_list, _ = svds(_adj.asfptype(), k=min(_adj.shape[0] - 1, 100))
        sv_list = np.sort(sv_list)[::-1]
        for i in range(sv_list.shape[0]):
            _svs[i+1] = sv_list[i]

        return _svs
        
    def plotDegDist(self):
        if self.real_adj_exist_flag:
            plt.scatter(self.degree_reals.keys(), self.degree_reals.values(), label="Real", s=100)
        plt.scatter(self.degree_ours.keys(), self.degree_ours.values(), label="Kronecker", s=60)
        plt.xlabel('Degree')
        plt.ylabel('Count')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.xlim([max(min(self.degree_ours.keys()) - 10, 0.5), max(self.degree_ours.keys()) + 100])
        plt.savefig(self.outputName + "_deg.png")
        plt.close()

    def plotDenDist(self):
        if self.real_adj_exist_flag:
            plt.scatter(self.density_real.keys(), self.density_real.values(), label="Real", s=100)
        plt.scatter(self.density.keys(), self.density.values(), label="Kronecker", s=60)
        plt.xlabel('Nodes')
        plt.ylabel('Edges')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.ylim([1, max(max(self.density.values()), max(self.density.values())) * 10])
        plt.xlim([1, max(max(self.density.keys()), max(self.density.keys())) * 10])
        plt.savefig(self.outputName + "_den.png")
        plt.close()

    def plotSvDist(self):
        max_y = 1
        if self.real_adj_exist_flag:
            plt.scatter(self.svs_real.keys(), self.svs_real.values(), label="Real", s=100)
            max_y = max(max_y, max(self.svs_real.values()) * 10)
        plt.scatter(self.svs.keys(), self.svs.values(), label="Kronecker", s=60)
        max_y = max(max_y, max(self.svs.values()) * 10)
        plt.scatter(self.svs.keys(), self.svs.values(), label="Kronecker", s=60)
        plt.xlabel('Rank')
        plt.ylabel('Singular Value')
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.ylim([1, max_y])
        plt.savefig(self.outputName + "_sv.png")
        plt.close()
