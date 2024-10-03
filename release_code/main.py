import argparse
from Kronecker import KProds
from StochasticKronecker import STKProds
from Analysis import Analysis
import time
import utils
import math

if __name__ == "__main__":

    # Parse the arguments
    parser = argparse.ArgumentParser(description="Generating kronecker graphs")
    parser.add_argument(
        "-f",
        "--fileName",
        action="store",
        default="data/input_cit-HepPh.txt",
        type=str,
        help="A file name for an initial matrix",
    )
    parser.add_argument(
        "-k",
        "--k",
        action="store",
        default=14,
        type=int,
        help="The number of Kroncker products",
    )
    parser.add_argument(
        "-o",
        "--outputName",
        action="store",
        default="cit-HepPh",
        type=str,
        help="A file name for an output matrix",
    )
    parser.add_argument(
        "-gf",
        "--graphFileName",
        action="store",
        default="data/cit-HepPh",
        type=str,
        help="A file name for a target graph",
    )
    parser.add_argument(
        "-s",
        "--stochastic",
        action="store_true",
        default=False,
        help="Enable the Stochastic Kronecker Model")
    args = parser.parse_args()
    
    # Read real-world graph
    real_adj= utils.read_graph(args.graphFileName)
            
    # Initialize the kronecker object
    if args.stochastic:
        kprods: STKProds = STKProds(k = args.k, real_adj=real_adj, filePath=args.fileName)
    else:
        kprods: KProds = KProds(k = args.k, filePath=args.fileName)

    print("Generation")
    # Generate a list of Kronecker graphs
    adj_list = kprods.produceGraph()

    print("Analysis")
    # Analyze the graph
    analysis: Analysis = Analysis(adj_list, real_adj, args.outputName)
    