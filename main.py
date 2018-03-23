from graph import Graph
import argparse
import random

def create_complete_graph(n, p):
    g = Graph()
    for i in range(n):
        g.add_vertex(str(i))
    # assert g.__graph['0'].vertex_degree == 0, 'test'

    # now add edges of complete graph with probability p
    for i in range(n):
        for j in range(n):
            if (i >= j): continue
            if random.random() <= p:
                # add an edge. Otherwise ignore.
                edges = (str(i), str(j))
                g.add_edge(edges)

                ## FIXME: not sure if i need this.
                # edges = (str(j), str(i))
                # g.add_edge(edges)
    return g
 
if __name__ == "__main__":
    # print("starting the graph percolation simulation")
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "-n", type=int, required=False,
                        default=3, help="number of vertices")
    parser.add_argument("-p", "-p", type=float, required=False,
                        default=1.0, help="percolation probability")
    # parser.add_argument("-kgraph", type=int, required=False,
                        # default=1, help="run k-graph simulation") 
    parser.add_argument("-hamiltonian", "-ham",  type=int, required=False,
                        default=0, help="run hamiltonian simulation") 
    parser.add_argument("-chromatic", "-chrom",  type=int, required=False,
                        default=0, help="run hamiltonian simulation") 

    args = parser.parse_args()
    g = create_complete_graph(args.n, args.p)
    
    # print("isolated: ", g.find_isolated_vertices())
    # print("delta: ", g.delta()) 
    # print("Delta: ", g.Delta()) 
    # print("connected: ", g.is_connected())
    # print("num edges: ", len(g.edges()))
    # print("diameter: ", g.diameter())
    # print(g.find_cycle("0"))
    
    if args.hamiltonian:
        if (g.find_cycle("0", cycle_len=len(g._graph))) is None:
            print("False")
        else:
            print("True")
    
    if args.chromatic:
        # print("going to test for chromatic num on complete graph")
        n = g.find_chromatic_num()
        print("chromatic number: ", n)
