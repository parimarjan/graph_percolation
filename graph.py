""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""
from collections import defaultdict
class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = defaultdict(list)
        self._graph = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self._graph.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self._graph, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self._graph:
            self._graph[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        # edge = set(edge)
        # vertex1 = edge.pop()
        # if edge:
            # # not a loop
            # vertex2 = edge.pop()
        # else:
            # # a loop
            # vertex2 = vertex1
        # if vertex1 in self._graph:
            # self._graph[vertex1].append(vertex2)
        # else:
            # self._graph[vertex1] = [vertex2]
        
        # just do undirected
        if edge[1] not in self._graph[edge[0]]:
            self._graph[edge[0]].append(edge[1])
        if edge[0] not in self._graph[edge[1]]:
            self._graph[edge[1]].append(edge[0])

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self._graph:
            for neighbour in self._graph[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self._graph:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def find_isolated_vertices(self):
        """ returns a list of isolated vertices. """
        graph = self._graph
        isolated = []
        for vertex in graph:
            if not graph[vertex]:
                isolated += [vertex]
        return isolated

    def find_path(self, start_vertex, end_vertex, path=[]):
        """ find a path from start_vertex to end_vertex 
            in graph """
        graph = self._graph
        path = path + [start_vertex]

        if start_vertex == end_vertex:
            return path

        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex, 
                                               end_vertex, 
                                               path)
                if extended_path: 
                    return extended_path
        return None
    
    def find_cycle(self, start_vertex, cycle_len=0, path=[]):
        """ find a path from start_vertex to end_vertex 
            in graph """
        graph = self._graph
        if start_vertex not in graph:
            return None

        if len(path) == 0:
            path = path + [start_vertex]

        cur_vertex = path[-1]

        for vertex in graph[cur_vertex]:
            found_cycle = vertex == start_vertex and len(path) >= cycle_len
            if found_cycle:
                path.append(start_vertex)
                return path

            if vertex not in path:
                path.append(vertex)
                extended_path = self.find_cycle(start_vertex,
                                               cycle_len, path)
                if extended_path:
                    return extended_path
        return None

    def valid_coloring(self, v, colours, c):
        '''
         A utility function to check if the current color assignment
         is safe for vertex v
        '''
        for other_v in self._graph[str(v)]:
            # if there colors match return false
            other_i = int(other_v)
            if colours[other_i] == c:
                return False

        return True


    def chrom_num_m_check(self, m, colours, v): 
        '''
        assumes v goes from 0 ... n-1
        '''
        if v == len(self._graph):
            return True

        for c in range(0, m):
            if self.valid_coloring(v, colours, c) == True:
                colours[v] = c
                if self.chrom_num_m_check(m, colours, v+1) == True:
                    return True
                colours[v] = 0
        return False

    def find_chromatic_num(self):
        '''
        try n = 0, 1, etc. and verify if a coloring is possible.
        '''
        colours = [-1] * len(self._graph)
        # give it a valid colouring to start
        for i in range(len(self._graph)):
            colours[i] = i

        chrom_num = -1
        for i in range(2, len(self._graph)+1):
            # chromatic numbers. start from 2
            if self.chrom_num_m_check(i, colours, 0):
                chrom_num = i
                break


        return chrom_num

    def find_all_paths(self, start_vertex, end_vertex, path=[]):
        """ find all paths from start_vertex to 
            end_vertex in graph """
        graph = self._graph 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.find_all_paths(vertex, 
                                                     end_vertex, 
                                                     path)
                for p in extended_paths: 
                    paths.append(p)
        return paths

    def is_connected(self, 
                     vertices_encountered = None, 
                     start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self._graph        
        vertices = gdict.keys() 
        if not start_vertex:
            # chosse a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex]:
                if vertex not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex):
                        return True
        else:
            return True
        return False

    def vertex_degree(self, vertex):
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. Loops are counted 
            double, i.e. every occurence of vertex in the list 
            of adjacent vertices. """ 
        adj_vertices =  self._graph[vertex]
        # degree = len(adj_vertices) + adj_vertices.count(vertex)
        degree = len(adj_vertices) 
        return degree

    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for vertex in self._graph:
            seq.append(self.vertex_degree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)

    @staticmethod
    def is_degree_sequence(sequence):
        """ Method returns True, if the sequence "sequence" is a 
            degree sequence, i.e. a non-increasing sequence. 
            Otherwise False is returned.
        """
        # check if the sequence sequence is non-increasing:
        return all( x>=y for x, y in zip(sequence, sequence[1:]))
  

    def delta(self):
        """ the minimum degree of the vertices """
        min = 100000000
        for vertex in self._graph:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min
        
    def Delta(self):
        """ the maximum degree of the vertices """
        max = 0
        for vertex in self._graph:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree > max:
                max = vertex_degree
        return max

    def density(self):
        """ method to calculate the density of a graph """
        g = self._graph
        V = len(g.keys())
        E = len(self.edges())
        return 2.0 * E / (V *(V - 1))

    def diameter(self):
        """ calculates the diameter of the graph """ 
        v = self.vertices() 
        pairs = [ (v[i],v[j]) for i in range(len(v)-1) for j in range(i+1, len(v))]
        smallest_paths = []
        for (s,e) in pairs:
            paths = self.find_all_paths(s,e)
            smallest = sorted(paths, key=len)[0]
            smallest_paths.append(smallest)

        smallest_paths.sort(key=len)

        # longest path is at the end of list, 
        # i.e. diameter corresponds to the length of this path
        diameter = len(smallest_paths[-1])
        return diameter

    @staticmethod
    def erdoes_gallai(dsequence):
        """ Checks if the condition of the Erdoes-Gallai inequality 
            is fullfilled 
        """
        if sum(dsequence) % 2:
            # sum of sequence is odd
            return False
        if Graph.is_degree_sequence(dsequence):
            for k in range(1,len(dsequence) + 1):
                left = sum(dsequence[:k])
                right =  k * (k-1) + sum([min(x,k) for x in dsequence[k:]])
                if left > right:
                    return False
        else:
            # sequence is increasing
            return False
        return True

   


if __name__ == "__main__":
    pass

    # g = { "a" : ["d"],
          # "b" : ["c"],
          # "c" : ["b", "c", "d", "e"],
          # "d" : ["a", "c"],
          # "e" : ["c"],
          # "f" : []
        # }

    # graph = Graph(g)
    # print(graph)

    # for node in graph.vertices():
        # print(graph.vertex_degree(node))

    # print("List of isolated vertices:")
    # print(graph.find_isolated_vertices())

    # print("""A path from "a" to "e":""")
    # print(graph.find_path("a", "e"))

    # print("""All pathes from "a" to "e":""")
    # print(graph.find_all_paths("a", "e"))

    # print("The maximum degree of the graph is:")
    # print(graph.Delta())

    # print("The minimum degree of the graph is:")
    # print(graph.delta())

    # print("Edges:")
    # print(graph.edges())

    # print("Degree Sequence: ")
    # ds = graph.degree_sequence()
    # print(ds)

    # fullfilling = [ [2, 2, 2, 2, 1, 1], 
                         # [3, 3, 3, 3, 3, 3],
                         # [3, 3, 2, 1, 1]
                       # ] 
    # non_fullfilling = [ [4, 3, 2, 2, 2, 1, 1],
                        # [6, 6, 5, 4, 4, 2, 1],
                        # [3, 3, 3, 1] ]

    # for sequence in fullfilling + non_fullfilling :
        # print(sequence, Graph.erdoes_gallai(sequence))

    # print("Add vertex 'z':")
    # graph.add_vertex("z")
    # print(graph)

    # print("Add edge ('x','y'): ")
    # graph.add_edge(('x', 'y'))
    # print(graph)

    # print("Add edge ('a','d'): ")
    # graph.add_edge(('a', 'd'))
    # print(graph)
