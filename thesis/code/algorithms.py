import copy
import math
import time
import datastructures

"""Implement the algorithms described by Widgerson in his paper
"Improving the Performance Guarantee for Approximate Graph Coloring"

Also implement the Structure-Driven Randomized version of the core
algorithms in the paper (B and D). Structure-Driven is a technique
currently in development at the Network and Data Science Laboratory
(NDS-Lab) of the Computer Research Center (IPN-CIC). It consists in
identify the property of a NP-Hard problem that an approximation
algorithm exploits (its 'structure') and perturb it inside the 
algorithm, with the purpose of (hopefully) improve the algorithm's
performance.

In the case of Graph coloring, the structure of the problem perturbed
inside the algorithm is that proposed by Widgerson, namely "if G is a
k-colorable graph, then for every vertex inside of it, the subgraph
induced by the neighborhood of that vertex is (k - 1)-colorable"; and
the perturbation consists in choosing any vertex with probability 
inversely proportional to its degree, instead of always choosing a
vertex of maximum (or minimum) degree. In the Structure-Driven 
Randomized version of the algorithm, every node has a probability of
being choosed at every step of the algorithm.

History:
    * 1.5
        - Now SDR methods use their own dictionary of colors, instead of
            the global COLORS and GREEDY_COLORS dictionaries. This was
            made since SDR methods are executed concurrently, and since
            interfere with each other.
        - Now BFS method restarts the flag of vertices before starting.
        - Modified the 'color' method to now accept an integer instead
            of a boolean to determine which coloring to use.
        - Modified the SDR family of algorithms to accept the 'exp' 
            float value to use in the PSO method.
        - Added the constant fields METHOD_RECURSIVE, METHOD_GREEDY and
            METHOD_SDR_GREEDY to choose between different colorings.
        - Added the sdr-widgerson method, which is the final version of
            the 'SDR' algorithmic family.
        - Added the WINNER_PROPOSAL_D global attribute to keep a record
            of the proposal that was choosed as the best one.
        - Now the 'sdr_e' algorithm doesn't print the results of the
            coloring, returning the number of colors used instead.
            
    * 1.4
        - Replaced the 'get_random_big_vertex' and 
            'get_random_small_vertex' methods with the unified method
            'get_random_vertex'.
        - Updated the SDR-E algorithm to choose between fixed and 
            iterated mode for SDR-C. Also now the proposals can
            be specified at the moment of calling.
        - Updated the SDR-D algorithm to work with different proposals.
    
    * 1.3 
        - Added the Fixed version of the SDR-C algorithm.
        
    * 1.2
        - Added the MAX_ITER value, to bound the execution of SDR
            algorithms.
            
    * 1.1
        - Added the Structure-Driven Randomized versions of all
            'Widgerson' algorithms (sdr_b, sdr_c, sdr_d and sdr_e).
            
    * 1.0 
        - Original script. Added the b, c, d, e, bfs, delta_coloring
            and sequential_coloring algorithms, and the color and f_k
            methods.

Attributes
    COLORS (dict): the dictionary that contains the vertices of a graph
      and the color assigned to it by the Widgerson algorithm.
    GREEDY_COLORS (dict): the dictionary that contains the vertices of
      a graph and the color assigned to it by the Greedy Independent
      Set algorithm.
    MAX_ITER (int): the maximum number of times a SDR-algorithm before
      declaring a failed execution.
    SCRIPT_VERSION (float): the current version of the script
    WINNER_PROPOSAL_D (int): the number of proposal to pick random
      vertices in the SDR-D algorithm which was choosed as the default
      option.
"""

COLORS = None
GREEDY_COLORS = None
SDR_GREEDY_COLORS = None
MAX_ITER = 100
SCRIPT_VERSION = 1.5
WINNER_PROPOSAL_C = 8
WINNER_PROPOSAL_D = 30

METHOD_RECURSIVE = 0
METHOD_GREEDY = 1
METHOD_SDR_GREEDY = 2

def b(k, graph, i, original=False):
    """Implements the B algorithm described by Widgerson in his paper.
    
    Algorithm B is used to color k-colorable graphs. Its input is an
    integer 'k', a k-colorable 'graph', and an integer 'i', telling the
    algorithm to color the 'graph' with successive colors i, i + 1, ...
    The output of the algorithm is the amount of colors used to color
    the 'graph'.
    
    Algorithm B colors any k-colorable graph on n vertices with at most
    2k * ceil(fk(n)) colors, and it is implemented to run in time 
    O(k(|V| + |E|)). For more information, please check the paper.
    
    Args:
      k (int): an integer k such that the graph is guaranteed to have
        a k-coloring.
      graph (GRAPH): a graph g coded in a GRAPH data structure.
      i (int): an integer which the algorithm will use to color the 
        graph with successive colors i, i + 1, etc.
        
    Complexity: O(k(|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
      
    Raises:
        RuntimeError: If the GRAPH given is not k-colorable.
    """
    # Step 0: Prepare the global COLORS array (if and only if this is
    # the original call
    if original:
        global COLORS
        COLORS = dict()
    
        for vertex in graph.vertices:
            COLORS[vertex.nid] = vertex.color
    
    # Step 1: Get the number of vertices
    n = len(graph.vertices)
    
    # Step 2: Base cases
    if k == 2:
        if bfs(graph, COLORS, i):
            return 2
        else:
            raise RuntimeError("Graph couldn't be 2-colored:\n{0}".format(
                str(graph)))
    
    if k >= math.log(n, 2):
        return sequential_coloring(graph, COLORS, i)
        
    # Step 3: Recursive Coloring Stage
    while graph.get_max_degree() >= math.ceil(f_k(k, n)):
        vertex = graph.get_max_degree_vertex()
        
        # Get the subgraph inducted by the chosen vertex's neighborhood
        h = graph.subgraph(vertex)
        
        # Stores the number of colors used by the recursive coloring
        j = b(k - 1, h, i)
        
        # Assign the chosen vertex its color
        vertex.color = i + j
        COLORS[vertex.nid] = vertex.color
        
        # Increase the amount of colors used
        i += j
        
        # Delete the chosen vertex from the graph
        graph.delete_vertex(vertex.nid)
        
    # Step 4: Brute force coloring stage
    # This instruction produces invalid colorings!
    # return delta_coloring(graph, i)
    
    # This instruction is proposed by me
    return (i + delta_coloring(graph, COLORS, i))


def bfs(graph, color_dict=None, color=0, root=None):
    """Use the Breadth First Search algorithm to 2-color a bipartite
    graph.
    
    If the graph is not bipartite, then the coloring fails.
    
    Args:
      graph (GRAPH): the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored. If not given, the
        default global COLORS dictionary will be used to store the 
        colors. Defaults to None.
      color (int): the label of the color that will be used to 2-color
        the graph. The graph will be colored with colors 'color' and
        'color + 1'. Defaults to 0.
      root (int): the Node ID of the vertex in which the search will
        begin. If not given, the first vertex on the graph's linked
        list will be used as the root. Defaults to None.
      
    Complexity: O(|V| + |E|)
      
    Returns:
      boolean: True if and only if the graph is 2-colored successfully.
        False if the graph is not bipartite (and therefore, the 
        coloring failed).
    """
    # For efficiency reasons, isolated vertices are colored first
    for vertex in graph.vertices:
        if len(vertex) == 0:
            # Marks the vertex and colors it
            vertex.color = color
            vertex.flag = True
            
            if color_dict is not None:
                color_dict[vertex.nid] = color
            else:
                COLORS[vertex.nid] = color
        # Restart vertex flag
        else:
            vertex.flag = False
            
    # It is possible for graphs to contain 
    # multiple connected components.
    for vertex in graph.vertices:
        # Only non-marked vertices start new trees
        if not vertex.flag:
            # Marks and colors the root
            vertex.flag = True
            vertex.color = color
                        
            # Saves the color into the global dictionary
            if color_dict is not None:
                color_dict[vertex.nid] = vertex.color
            else:
                COLORS[vertex.nid] = vertex.color
        
            # Creates the queue used to store the vertices
            queue = datastructures.DoublyLinkedList()
            
            # Adds the root to queue
            queue.append(datastructures.Node(vertex.nid))
            
            # Performs BFS 
            while not queue.is_empty():
                # Get the first node on the queue
                current = graph.vertices[queue.remove_first().nid]
                
                # Checks the adjacency list of the current node
                for neighbor_nid in current.data:
                    # Get the reference to the neighbor
                    neighbor = graph.vertices[neighbor_nid.nid]
                
                    # Checks if node is already marked
                    if not neighbor.flag:
                        # Marks and colors the neighbor
                        neighbor.flag = True
                        
                        # Alterns color to use
                        if current.color == color:                            
                            neighbor.color = color + 1
                        else:
                            neighbor.color = color
                            
                        # Saves the color into the global dictionary
                        if color_dict is not None:
                            color_dict[neighbor.nid] = neighbor.color
                        else:
                            COLORS[neighbor.nid] = neighbor.color
                            
                        # Adds the neighbor to queue
                        queue.append(datastructures.Node(neighbor.nid))
                    
                    # If the vertex has already been marked, cheks colors
                    else:
                        # If both colors are equal, the coloring fails
                        if current.color == neighbor.color:
                            return False
    
    # If we reach this part, the coloring was successful
    return True


def c(graph):
    """Implements the C algorithm described by Widgerson in his paper.
    
    Algorithm C is used to color any graph where the chromatic number
    is not known. It calls algorithm B with increasingly higher values
    of k until it is able to find a proper coloring.
    
    Algorithm C colors any graph on n vertices with at most
    2 * chi(G) * ceil(n ^ 1 - 1 / (chi(G) - 1)) colors, 
    and it is implemented to run in time 
    O(|V| + |E|) * chi(G) * log2(chi(G)), where chi(G) is the chromatic
    number of graph G. For more information, please check the paper.
    
    Args:
      graph (GRAPH): the graph to color.
        
    Complexity: O(chi(G) * log2(chi(G)) * (|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
    """
    colored = False
    exponent = 1
    
    while not colored:
        # Creates a copy of the graph
        copy_graph = copy.deepcopy(graph)
        
        try:
            result = b(2 ** exponent, copy_graph, 1, True)            
            colored = True
        except RuntimeError:        
            exponent += 1
            colored = False
            
    # Use binary search to look for k0
    lower = 2 ** (exponent - 1)
    upper = 2 ** exponent
    
    while abs(upper - lower) > 1:
        copy_graph = copy.deepcopy(graph)
        middle = (lower + upper) // 2
        
        try:
            result = b(middle, copy_graph, 1, True)
            upper = middle
        except RuntimeError:
            lower = middle

    # Colors the graph using k0
    try:
        copy_graph = copy.deepcopy(graph)
        result = b(lower, copy_graph, 1, True)
    except RuntimeError:
        copy_graph = copy.deepcopy(graph)    
        result = b(upper, copy_graph, 1, True)
    
    max_color = 0
    
    for v in copy_graph.vertices:
        if v.color > max_color:
            max_color = v.color
    
    return max_color


def color(graph, colors_dict):
    """Assigns the vertices of the given GRAPH with their respective
    colors.
    
    Two arrays of colors are keeped: the COLORS array used by the
    Widgerson algorithm, and the GREEDY_COLORS array used by the 
    Greedy Independent Set algorithm. This is done in order to decide
    which one of the two colorings is better, and assign the best
    coloring to the graph.
    
    Since this method visits every node, its complexity is O(|V|)
    
    Args:
      graph (GRAPH): The graph to color.
      colors (dictionary): a Python dictionary from which the colors
        will be taken.
        
    Complexity: O(|V|)
    """
    for vid in colors_dict.keys():
        graph.vertices[vid].color = colors_dict[vid]


def d(graph, color_dict=None):
    """Implement the Greedy Independent Set algorithm for graph 
    coloring.
    
    The Greedy Independent Set (here called algorithm D) consists in
    coloring minimum degree vertex with a given color, delete its
    neighbors, and proceed until no vertex can be assigned with that
    color, moment when a new color is used and the process starts 
    again, until all vertices of the graph have been colored.
    
    The complexity of the Greedy Independent Set is O(|V| ^ 2).
    
    Args:
      graph (GRAPH): the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored. If not given, the 
        defaut global GREEDY_COLORS dictionary will be used. Defaults
        to None.
      
    Complexity: O(|V| ^ 2)
      
    Returns:
      int: The number of colors that the algorithm used to color the
        graph.
    """
    # Create global dictionary only if no dictionary is provided.
    if color_dict is None:
        global GREEDY_COLORS
        GREEDY_COLORS = dict()
    
    # The color to use
    i = 1
    
    copy_graph = copy.deepcopy(graph)
    copy_graph.build_DEGREE()
    
    while not copy_graph.vertices.is_empty():
        uncolored = copy.deepcopy(copy_graph)
        uncolored.build_DEGREE()
        
        while not uncolored.vertices.is_empty():
            # Color a minimum degree vertex with current color
            vertex = uncolored.get_min_degree_vertex()
            if color_dict is not None:
                color_dict[vertex.nid] = i
            else:
                GREEDY_COLORS[vertex.nid] = i
            
            # Delete the vertex and its neighborhood
            for neighbor in vertex.data:
                # Delete the edges with the neighborhood
                for other_neighbor in uncolored.vertices[neighbor.nid].data:
                    uncolored.degrees.decrease(
                        uncolored.vertices[neighbor.nid])
                    uncolored.degrees.decrease(
                        uncolored.vertices[other_neighbor.nid])
                    uncolored.delete_edge(neighbor.nid, other_neighbor.nid)
                            
                # Also delete the edge with the neighbor in the copy graph
                copy_graph.degrees.decrease(copy_graph.vertices[vertex.nid])
                copy_graph.degrees.decrease(copy_graph.vertices[neighbor.nid])
                copy_graph.delete_edge(vertex.nid, neighbor.nid)
            
                # Now delete the neighbor
                neighbor_bucket = len(uncolored.vertices[neighbor.nid])
                uncolored.degrees.buckets[neighbor_bucket].data.remove(
                    neighbor.nid)
                uncolored.delete_vertex(neighbor.nid)
                        
            # Delete the colored vertex from its bucket
            uncolored.degrees.buckets[len(vertex)].data.remove(vertex.nid)
            
            # Finally, delete the min degree vertex from both graphs
            uncolored.delete_vertex(vertex.nid)
            
            original_vertex = copy_graph.vertices[vertex.nid]
            
            # Delete remaining edges
            for neighbor in original_vertex.data:
                copy_graph.degrees.decrease(
                    copy_graph.vertices[neighbor.nid])
                copy_graph.degrees.decrease(
                    copy_graph.vertices[original_vertex.nid])
                copy_graph.delete_edge(original_vertex.nid, neighbor.nid)
            
            copy_graph.degrees.buckets[len(original_vertex)].data.remove(
                vertex.nid)
            copy_graph.delete_vertex(original_vertex.nid)
            
        # Create a new color
        i += 1
        
    return (i - 1)


def delta_coloring(graph, color_dict=None, color=0):
    """Colors the given graph with at most delta(GRAPH) + 1 colors.
    
    This method assigns delta(GRAPH) colors to the neighborhood of
    a vertex of maximum degree, where delta(GRAPH) is the maximum
    degree of GRAPH.
    
    Since all nodes on the graph are colored, and the adjacency list
    of every one of them is also checked, the complexity of the delta
    coloring is O(|V| + |E|).
    
    Args:
      graph (GRAPH): the graph to be colored
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be saved. If not given, the
        default global COLORS dictionary will be used. Defaults to
        None.
      color (int): the initial color to use. Defaults to zero.
      
    Complexity: O(|V| + |E|)
      
    Returns:
      int: The amount of colors used to color GRAPH (that is,
        delta(GRAPH) + 1).
        
    Raises:
        RuntimeError: If more than delta(GRAPH) + 1 colors are used in
            the coloring (where delta(GRAPH) is the maximum degree 
            occurring in the GRAPH).
    """
    colors_used = 0
    
    for vertex in graph.vertices:
        current_color = color
        
        while not graph.is_valid(vertex.nid, current_color):
            current_color += 1
            
        if current_color - color > colors_used:
            colors_used = current_color - color
            
        if colors_used > graph.get_max_degree() + 1:
            raise RuntimeError(
                "Too many colors used in Brute Force coloring stage!")
            
        vertex.color = current_color
        
        if color_dict is not None:
            color_dict[vertex.nid] = vertex.color
        else:
            COLORS[vertex.nid] = vertex.color
        
    return colors_used


def e(graph):
    """Implement the Widgerson algorithm.
    
    This method calls the Recursive coloring algorithm C and the
    Greedy Independent Set algorithm D, and produces as output the
    coloring that used less colors.
    
    The GRAPH's vertices are colored using the algorithm that used
    fewer color, and since both algorithms C and D use copies of the
    GRAPH, the given GRAPH is not modified (except for the coloring).
    
    Since this method executes both C and D algorithms, its complexity
    is O(chi(G) * log2(chi(g)) * (|V| + |E|)), the same as algorithm C.
    
    Args:
      graph (GRAPH) the graph to color.
      
    Complexity: O(chi(G) * log2(chi(G)) * O(|V| + |E|))
    """
    recursive_colors = c(graph)
    greedy_colors = d(graph)
    
    #if recursive_colors <= greedy_colors:
    #    color(graph)
    #    print("{0} | [ {1} / {2} ]".format(
    #      str(recursive_colors).rjust(2), 
    #      str(recursive_colors).rjust(2), 
    #     str(greedy_colors).rjust(2)))
    #else:
    #    color(graph, True)
    #    print("{0} | [ {1} / {2} ]".format(
    #      str(greedy_colors).rjust(2), 
    #      str(recursive_colors).rjust(2), 
    #      str(greedy_colors).rjust(2)))
    
    return min(recursive_colors, greedy_colors)


def f_k(k, x):
    """Implements the special function f_k defined by Widgerson.
    
    In his paper, Widgerson defined f_k as
    
                f_k(x) = x ^ (1 - 1/(k - 1))
                
    Args:
      k (int): the first argument of the function.
      x (int): the second argument of the function.
      
    Complexity: O(1)
      
    Returns:
      float: f_k(x), with f_k equal to the function described above.
    """
    return x ** (1 - 1 / (k - 1))


def sdr_b(k, graph, i, color_dict, proposal=0, exp=1):
    """Implements the Structure-Driven Randomized version of the B 
    algorithm described by Widgerson in his paper.
    
    Algorithm B is used to color k-colorable graphs. Its input is an
    integer 'k', a k-colorable 'graph', and an integer 'i', telling the
    algorithm to color the 'graph' with successive colors i, i + 1, ...
    The output of the algorithm is the amount of colors used to color
    the 'graph'.
    
    The Structure-Driven version modifies the algorithm so that every
    vertex has some probability of being choosed at every call to the
    algorithm, not only a maximum degree vertex. The vertices are 
    choosed with help of a pseudo-random number generator, and hence
    the name.
    
    There's currently no performance guarantee demonstrated for the
    SDR_B algorithm, however its running time is still O(k(|V| + |E|)).
    
    Args:
      k (int): an integer k such that the graph is guaranteed to have
        a k-coloring.
      graph (GRAPH): a graph g coded in a GRAPH data structure.
      i (int): an integer which the algorithm will use to color the 
        graph with successive colors i, i + 1, etc.
      color_dict (dictionary) a Python dictionary in which the colors
        used by the algorithm will be stored.
      proposal (int): tells the algorithm which proposal to select
        random vertices to use. Defaults to 0.
      exp (float): the exponent to which the formula for choosing
        random vertices will be raised. Defaults to 1.
        
    Complexity: O(k(|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
  
    Raises:
      RuntimeError: If the given GRAPH is not k-colorable.
    """
    # Step 1: Get the number of vertices
    n = graph.m
    
    # Step 2: Base cases
    if n == 0:
        return 0
        
    if k == 2:
        if bfs(graph, color_dict, i, None):
            return 2
        else:
            raise RuntimeError("Graph couldn't be 2-colored!")
    
    if k >= math.log(n, 2):
        return sequential_coloring(graph, color_dict, i)
        
    # Step 3: Recursive Coloring Stage
    while graph.get_max_degree() >= math.ceil(f_k(k, n)):
        vertex = graph.get_random_vertex(proposal, exp)
        
        # Get the subgraph inducted by the chosen vertex's neighborhood
        h = graph.subgraph(vertex)
        
        # Stores the number of colors used by the recursive coloring
        j = sdr_b(k - 1, h, i, color_dict, proposal, exp)
        
        # Assign the chosen vertex its color
        vertex.color = i + j
        color_dict[vertex.nid] = vertex.color
        
        # Increase the amount of colors used
        i += j
        
        # Delete the chosen vertex from the graph
        graph.delete_vertex(vertex.nid)
        
    # Step 4: Brute force coloring stage
    # The following instruction causes invalid colorings!
    # return delta_coloring(graph, i)
    
    # This instruction is proposed by me
    return (i + delta_coloring(graph, color_dict, i))


def sdr_c(
  graph,
  color_dict,
  iterated=True, 
  proposal=WINNER_PROPOSAL_C, 
  seed=None, 
  expc=1):
    """Implements the Structure-Driven Randomized version of the C 
    algorithm described by Widgerson in his paper.
    
    Algorithm C is used to color any graph where the chromatic number
    is not known. It calls algorithm B with increasingly higher values
    of k until it is able to find a proper coloring.
    
    The Structure-Driven version modifies the algorithm so that every
    vertex has some probability of being choosed at every call to the
    algorithm, not only a maximum degree vertex. The vertices are 
    choosed with help of a pseudo-random number generator, and hence
    the name.
    
    There's currently no performance guarantee demonstrated for the
    SDR_C algorithm, however its running time is still 
    O(|V| + |E|) * chi(G) * log2(chi(G), where chi(G) is the chromatic
    number of graph G. For more information, please check the paper.
    
    Args:
      graph (GRAPH): the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be saved.
      iterated (boolean): indicates the mode in which the SDR-C 
        algorithm will be executed. If True, the Iterated version
        will be used, whereas the Fixed mode will be used if False.
      proposal (int): Indicates the Proposal to use at the moment of
        choosing the random vertices during the execution of the
        algorithm. If not given, uniform probability will be used.
        Defaults to 0 (zero).
      seed (int): the seed to use for the pseudo-random number 
        generator in the Fixed mode. If not given, current system time
        will be used as seed. Defaults to None.
      expc (float): the exponent to which the formula for choosing 
        random vertices will be raised. Defaults to 1.
        
    Complexity: O(chi(G) * log2(chi(G)) * (|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
    """
    # Sets current time as seed if seed is not given.
    if seed is None:
        seed = time.time()
        
    # Calls the appropriate version of the algorithm
    if iterated:
        return sdir_c(graph, color_dict, proposal, expc)
    else:
        return sdfr_c(graph, color_dict, proposal, seed, expc)


def sdr_d(graph, color_dict, proposal=WINNER_PROPOSAL_D, expd=1):
    """Implement the Structure-Driven Randomized version of the Greedy
    Independent Set algorithm for graph coloring.
    
    The Greedy Independent Set (here called algorithm D) consists in
    coloring minimum degree vertex with a given color, delete its
    neighbors, and proceed until no vertex can be assigned with that
    color, moment when a new color is used and the process starts 
    again, until all vertices of the graph have been colored.
    
    However, the Structure-Driven version chooses a vertex with
    probability inversely proportional to its degree, instead of 
    always choosing a minimum degree vertex.
    
    The complexity of the Greedy Independent Set is O(|V| ^ 2).
    
    Args:
      graph (GRAPH) the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored.
      proposal (int): the number of proposal to choose for choosing
        random vertices. Defaults to zero.
      expd (int): the exponent to which the formula for choosing
        random vertices will be raised. Defaults to 1.
      
    Complexity: O(|V| ^ 2)
      
    Returns:
      int: The number of colors that the algorithm used to color the
        graph.
    """
    # The color to use
    i = 1
    
    copy_graph = copy.deepcopy(graph)
    copy_graph.build_DEGREE()
    
    while not copy_graph.vertices.is_empty():
        uncolored = copy.deepcopy(copy_graph)
        uncolored.build_DEGREE()
        
        while not uncolored.vertices.is_empty():
            # Color a minimum degree vertex with current color
            vertex = uncolored.get_random_vertex(proposal, expd)

            color_dict[vertex.nid] = i
            
            # Delete the vertex and its neighborhood
            for neighbor in vertex.data:
                # Delete the edges with the neighborhood
                for other_neighbor in uncolored.vertices[neighbor.nid].data:
                    uncolored.degrees.decrease(
                        uncolored.vertices[neighbor.nid])
                    uncolored.degrees.decrease(
                        uncolored.vertices[other_neighbor.nid])
                    uncolored.delete_edge(neighbor.nid, other_neighbor.nid)
                            
                # Also delete the edge with the neighbor in the copy graph
                copy_graph.degrees.decrease(copy_graph.vertices[vertex.nid])
                copy_graph.degrees.decrease(copy_graph.vertices[neighbor.nid])
                copy_graph.delete_edge(vertex.nid, neighbor.nid)
            
                # Now delete the neighbor
                neighbor_bucket = len(uncolored.vertices[neighbor.nid])
                uncolored.degrees.buckets[neighbor_bucket].data.remove(
                    neighbor.nid)
                uncolored.delete_vertex(neighbor.nid)
                        
            # Delete the colored vertex from its bucket
            uncolored.degrees.buckets[len(vertex)].data.remove(vertex.nid)
            
            # Finally, delete the min degree vertex from both graphs
            uncolored.delete_vertex(vertex.nid)
            
            original_vertex = copy_graph.vertices[vertex.nid]
            
            # Delete remaining edges
            for neighbor in original_vertex.data:
                copy_graph.degrees.decrease(
                    copy_graph.vertices[neighbor.nid])
                copy_graph.degrees.decrease(
                    copy_graph.vertices[original_vertex.nid])
                copy_graph.delete_edge(original_vertex.nid, neighbor.nid)
            
            copy_graph.degrees.buckets[len(original_vertex)].data.remove(
                vertex.nid)
            copy_graph.delete_vertex(original_vertex.nid)
            
        # Create a new color
        i += 1
        
    return (i - 1)


def sdr_e(graph, 
  iterated=True, 
  cprop=WINNER_PROPOSAL_C, 
  dprop=WINNER_PROPOSAL_D, 
  seed=None):
    """Implement the Structure-Driven Randomized Widgerson algorithm.
    
    This method calls the Structure-Driven versions of the Recursive 
    coloring Structure-Driven Randomized algorithm SDR-C and the Greedy
    Independent Set Structure-Driven Randomized algorithm SDR-D, and
    produces as output the coloring that used less colors.
    
    The GRAPH's vertices are colored using the algorithm that used
    fewer color, and since both algorithms SDR-C and SDR-D use copies
    of the GRAPH, the given GRAPH is not modified (except for the 
    coloring).
    
    Since this method executes both SDR-C and SDR-D algorithms, its 
    complexity is O(chi(G) * log2(chi(g)) * (|V| + |E|)), the same 
    as algorithm SDR-C.
    
    Args:
      graph (GRAPH): the graph to color.
      iterated (boolean): specifies the mode in which the SDR-C
        algorithm will be executed: if True, the SDIR-C algorithm
        (iterated mode) will be used, whereas SDFR-C algorithm 
        (fixed mode) will be used if False. Defaults to True.
      cprop (int): indicates the Proposal that will be used to
        choose random vertices in the SDR-C algorithm. Defaults
        to zero (0).
      dprop (int): indicates the Proposal that will be used to
        choose random vertices in the SDR-D algorithm. Defaults
        to zero (0).
      seed (int): sets the seed for the experiment. If not given,
        the current system time at the moment of calling will be
        used as seed. Defaults to None.
      
    Complexity: O(chi(G) * log2(chi(G)) * (|V| + |E|))
    """
    # Sets the current system time as seed if seed is not given
    if seed is None:
        seed = time.time()
    
    # Creates the dictionaries to store the colors
    rdict = dict()
    gdict = dict()
    
    # Selects mode to execute SDR-C
    recursive_colors = sdr_c(graph, rdict, iterated, cprop, seed)
    greedy_colors = sdr_d(graph, gdict, dprop)
          
    winner = min(recursive_colors, greedy_colors)
    
    if winner == recursive_colors:
        color(graph, METHOD_RECURSIVE, rdict)
    else:
        color(graph, METHOD_SDR_GREEDY, gdict)
          
    return winner


def sdr_widgerson(graph, expc=1, expd=1):
    """Implement the final version of the SDR-Widgerson algorithm.
    
    The SDR-Widgerson (Structure-Driven Randomized Widgerson) algorithm
    is a new version of the algorithm which, hopefully, improves the
    performance of the original algorithm.
    
    Args:
      graph (GRAPH): the graph to color.
      expc (float): the exponent to which the formula for the SDR-C
        algorithm will be raised. Defaults to 1.
      expd (float): the exponent to which the formula for the SDR-D
        algorithm will be raised. Defaults to 1.
      
    Returns:
      int: the number of colors used to color the graph.
    """
    # Creates the dictionaries to store the colors
    greedy_dict = dict()
    sdr_greedy_dict = dict()
    sdr_recursive_dict = dict()
    
    # Executes the algorithms
    greedy_colors = d(graph, greedy_dict)
    sdr_greedy_colors = sdr_d(
      graph, sdr_greedy_dict, WINNER_PROPOSAL_D, expd
    )
    
    try:
        sdr_recursive_colors = sdr_c(
          graph, sdr_recursive_dict, WINNER_PROPOSAL_C, None, expc
        )
    except RuntimeError:
        sdr_recursive_colors = 2 ** 63
    
    winner = min(greedy_colors, sdr_recursive_colors, sdr_greedy_colors)
    
    if winner == greedy_colors:
        color(graph, greedy_dict)
    elif winner == sdr_recursive_colors:
        color(graph, sdr_recursive_dict)
    elif winner == sdr_greedy_colors:
        color(graph, sdr_greedy_dict)
    
    return winner


def sdir_c(graph, color_dict, proposal=WINNER_PROPOSAL_C, expc=1):
    """Implements the Structure-Driven Iterated Randomized version of
    the C algorithm described by Widgerson in his paper.
    
    Algorithm C is used to color any graph where the chromatic number
    is not known. It calls algorithm B with increasingly higher values
    of k until it is able to find a proper coloring.
    
    The Structure-Driven version modifies the algorithm so that every
    vertex has some probability of being choosed at every call to the
    algorithm, not only a maximum degree vertex. The vertices are 
    choosed with help of a pseudo-random number generator, and hence
    the name.
    
    Given the nature of the algorithm, randomization may sometimes
    leave to a failed execution when a 'bad' sequence of vertex is
    choosed. The Iterated version of the SDR-C algorithm solves this
    problem by executing itself until a good coloring can be found.
    
    There's currently no performance guarantee demonstrated for the
    SDR_C algorithm, however its running time is still 
    O(|V| + |E|) * chi(G) * log2(chi(G), where chi(G) is the chromatic
    number of graph G. For more information, please check the paper.
    
    Args:
      graph (GRAPH): the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored.
      proposal (int): the number of proposal to use to choose random
        vertices. Defaults to zero.
      expc (float): the exponent to which the formula for choosing
        random vertices of the graph will be raised. Defaults to 1.
        
    Complexity: O(chi(G) * log2(chi(G)) * (|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
    """
    colored = False
    count = 0
    exponent = 1
    
    while not colored:
        # Creates a copy of the graph
        copy_graph = copy.deepcopy(graph)
        
        try:
            result = sdr_b(2 ** exponent, copy_graph, 1, color_dict, proposal, expc)
            colored = True
        except RuntimeError:        
            exponent += 1
            colored = False
            
    # Use binary search to look for k0
    lower = 2 ** (exponent - 1)
    upper = 2 ** exponent
    
    while abs(upper - lower) > 1:
        copy_graph = copy.deepcopy(graph)
        middle = (lower + upper) // 2
        
        try:
            result = sdr_b(middle, copy_graph, 1, color_dict, proposal, expc)
            upper = middle
        except RuntimeError:
            lower = middle
    
    colored = False
    
    # Colors the graph using k0. Due to randomness, it is possible to get
    # invalid executions
    while not colored and count < MAX_ITER:
        try:
            try:
                copy_graph = copy.deepcopy(graph)
                result = sdr_b(lower, copy_graph, 1, color_dict, proposal, expc)
                colored = True
            except RuntimeError:
                copy_graph = copy.deepcopy(graph)
                result = sdr_b(upper, copy_graph, 1, color_dict, proposal, expc)
                colored = True
        except RuntimeError:
            colored = False
            count += 1
    
    if not colored:
        raise RuntimeError(
          "Graph couldn't be colored! More iterations are needed"
        )
    
    max_color = 0
    
    for vid, clr in color_dict.items():
        if clr > max_color:
            max_color = clr
    
    return max_color


def sdfr_c(graph, color_dict, proposal=WINNER_PROPOSAL_C, seed=0, expc=1):
    """Implements the Structure-Driven Fixed Randomized version of the
    C algorithm described by Widgerson in his paper.
    
    Algorithm C is used to color any graph where the chromatic number
    is not known. It calls algorithm B with increasingly higher values
    of k until it is able to find a proper coloring.
    
    The Structure-Driven version modifies the algorithm so that every
    vertex has some probability of being choosed at every call to the
    algorithm, not only a maximum degree vertex. The vertices are 
    choosed with help of a pseudo-random number generator, and hence
    the name.
    
    Given the nature of the algorithm, randomization may sometimes
    leave to a failed execution when a 'bad' sequence of vertex is
    choosed. The Fixed version of the SDR-C algorithm sets the seed
    everytime the algorithm SDR-B is called, thus given the algorithm
    a more 'deterministic' approach.
    
    There's currently no performance guarantee demonstrated for the
    SDR_C algorithm, however its running time is still 
    O(|V| + |E|) * chi(G) * log2(chi(G), where chi(G) is the chromatic
    number of graph G. For more information, please check the paper.
    
    Args:
      graph (GRAPH): the graph to color.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored.
      proposal (int): the number of proposal that will be used to
        to choose the random vertices. If not given, the default
        proposal '0' (zero) is used. Defaults to zero.
      seed (int): the seed that will be used for the pseudo-random
        number generator. If not given, '0' (zero) will be used as
        seed. Defaults to zero.
      expc (int): the exponent to which the formula for choosing random
        vertices will be raised to. Defaults to 1.
        
    Complexity: O(chi(G) * log2(chi(G)) * (|V| + |E|))
        
    Returns:
      int: the number of colors the algorithm used to color the
      'graph'.
    """
    colored = False
    count = 0
    exponent = 1
    
    while not colored:
        # Creates a copy of the graph
        copy_graph = copy.deepcopy(graph)
        
        try:
            copy_graph.set_seed(seed)
            result = sdr_b(2 ** exponent, copy_graph, 1, color_dict, proposal, expc)
            colored = True
        except RuntimeError:        
            exponent += 1
            colored = False
            
    # Use binary search to look for k0
    lower = 2 ** (exponent - 1)
    upper = 2 ** exponent
    
    while abs(upper - lower) > 1:
        copy_graph = copy.deepcopy(graph)
        copy_graph.set_seed(seed)
        middle = (lower + upper) // 2
        
        try:
            result = sdr_b(middle, copy_graph, 1, color_dict, proposal, expc)
            upper = middle
        except RuntimeError:
            lower = middle
    
    # Colors the graph using k0.
    try:
        copy_graph = copy.deepcopy(graph)
        copy_graph.set_seed(seed)
        result = sdr_b(lower, copy_graph, 1, color_dict, proposal, expc)
    except RuntimeError:
        copy_graph = copy.deepcopy(graph)
        copy_graph.set_seed(seed)
        result = sdr_b(upper, copy_graph, 1, color_dict, proposal, expc)
    
    color(graph)
    max_color = 0
    
    for vid, clr in color_dict.items():
        if clr > max_color:
            max_color = clr
    
    return max_color


def sequential_coloring(graph, color_dict=None, color=0):
    """Color the graph sequentially, assigning each node with a unique
    color.
    
    This method is used by Widgerson when Algorithms B, C, and E try to
    color a graph with a number of colors k equal to or higher than the
    base 2 logarithm of the number of vertices in the graph.
    
    Since this algorithm requires to visit each node, its complexity is
    always O(|V|).
    
    Args:
      graph (GRAPH): the graph to be colored.
      color_dict (dictionary): a Python dictionary in which the colors
        assigned by the algorithm will be stored. If not given, the
        default global COLORS array will be used. Defaults to None.
      color (int): the initial color to use. Graph will be colored 
        using sequentially increasing colors starting from this value.
        Defaults to zero.
    
    Complexity: O(|V|)
    
    Returns:
      The number of colors used to color the graph (that is, the number
      of vertices inside the graph).
    """
    colors_used = 0
    
    for vertex in graph.vertices:
        vertex.color = color + colors_used
        
        if color_dict is not None:
            color_dict[vertex.nid] = vertex.color
        else:
            COLORS[vertex.nid] = vertex.color
            
        colors_used += 1
        
    return colors_used
