"""Implement the data structures described by Widgerson in his paper
"Improving the Performance Guarantee for Approximate Graph Coloring".

Node and DoublyLinkedList are the core structures. Node is an abstract
container to hold data in a doubly linked list. DoublyLinkedList, as
the name implies, is a doubly linked list which has been modified to
include a dictionary structure to hold its elements, which allows to
achieve greater efficiency than a regular doubly linked list.

GRAPH is used, as the name implies, to represent graphs. GRAPH has a
doubly linked list for the vertices. Each vertex points to its
adjacency list, which is also doubly linked. In addition if (u, w) is
an edge of the graph, then w on u's list will point to u on w's list
and vice versa.

DEGREE is used to maintain the degree of each vertex, so that it
can be updated in constant time with each removal of an edge, and
have a constant time access to a vertex of maximum degree.

Attributes:
  SCRIPT_VERSION (float): the current version of the script.
  SENTINEL (int) : a sentinel value, used to denote illegal values.
  
History:
    * 1.5
        - Added the 'from_json' method, that allows to fully recreate
            GRAPHS stored in JSON format.
        - Added the 'to_json' method, that allows to store GRAPHS data
            structures in JSON format.

    * 1.4
        - Added the GRAPH's 'check_coloring' method, to quickly check
            if a coloring is valid or not.
        - Replaced the 'get_random_big_vertex' and 
            'get_random_small_vertex' methods with a unified method,
            'get_random_vertex'.
        - Added the proposals to choose random small vertices
            (Proposals 29 - 36).
            
    * 1.3
        - Corrected errors on the proposals for choosing random
            vertices (Proposals 1 - 28).
        - Modified the GRAPH's 'delete_edge' method to only decrease
            the GRAPH's number of edges m if an edge is actually 
            deleted.
        - Added the 'to_dimacs' method to export graphs to the DIMACS
            format.

    * 1.2
        - Added the GRAPH 'get_random_small_vertex' method to choose
            a vertex with probability inversely proportional to its
            degree.
        - Added the GRAPH 'get_random_big_vertex' method to choose a
            vertex with probability proportional to its degree.
        - Added the GRAPH 'm' attribute, that holds the number of
            vertices whithin the graph.
        - Added the GRAPH 'n' attribute, that holds the number of 
            edges within the graph.
        - Added the different proposals to choose random vertices
            (Proposals 1 - 28).
        - Modified the GRAPH 'add_vertex' and 'delete_vertex'
            methods, to update the 'm' attribute everytime they are
            called.
        - Modified the GRAPH 'add_edge' and 'delete_edge' methods, to
            update the 'n' attribute everytime they are called.
            
    * 1.1 
        - Added the GRAPH '__deepcopy__' method to allow deep copies
            to use in the algorithms, since their destructive nature
            rendered the original graph unusable.
        - Added the GRAPH '__repr__' method to generate JSON 
            representations of GRAPH's, fully compatible with the
            Java Graph Viewer Engine.
        - Added the GRAPH 'is_valid' method to check if a given color
            can be assigned to a Node without generating conflicts.
        - Added the GRAPH 'get_min_degree' method to get constant time
            access to the minimum degree currently present in the 
            GRAPH.
        - Added the GRAPH 'get_min_degree_vertex' method to get a 
            constant time access to a reference to a minimum degree
            vertex in the GRAPH.
        - Added the GRAPH 'print_colors' method to quickly check the
            coloring of the graph.
        - Added the 'from_dimacs' utility method to generate GRAPHS 
            given in the DIMACS format.
        - Added the Node '__repr__' method to represent nodes in the
            JSON format, compatible with the Java Graph Viewer Engine.
        - Added the Node 'flag' attribute for use in search algorithms.
        - Added the Node 'color' attribute to store the color assigned
            to it by a coloring algorithm.
        - Added the DEGREE 'min_degree' attribute to store the minimum
            degree currently present in the associated GRAPH.
        - Modified the Node '__str__' method to include the color and
            flag in the representation.
        - Modified the GRAPH 'induct' method name to 'subgraph' to
            better reflect the behavior of the method.
        - Modified the GRAPH 'subgraph' method to perform a better 
            search for maximum/minimum degree vertices while creating
            the induced subgraph.
        - Modified the GRAPH 'get_max_degree_vertex' method to look
            for vertices in other buckets when the 'max_degree' bucket
            gets empty.

    * 1.0 Original script. Added Nodes, DoublyLinkedLists, GRAPHS and
            DEGREES.
"""

import json
import random

SCRIPT_VERSION = 1.5
SENTINEL = 2 ** 63 - 1


class Node(object):
    """Represent the basic unit of a doubly linked list.
    
    Each node has two components: a 'head' and a 'tail'. The 'head' is
    the pointer to the node that is inmediatly before the node on the
    list, while the 'tail' is the pointer to the node that comes
    inmediatly after the node. You can picture nodes in a doubly linked
    list as a group of elephants standing in line: an elephant grabs 
    the tail of the elephant that is in front of it using its trunk 
    (head), while its own tail is grabbed by the elephant that is 
    behind it.
    
    Additionally, nodes have a Node ID to uniquely identify them within
    a linked list; a pointer called 'data', that can be used to store 
    any object, such as other nodes, sets, tuples or inclusive other 
    lists; a pointer called 'bucket', that is used to link nodes to
    other nodes in a different data structure called DEGREE, and a 
    'color' attribute that can be used to store the color of the node
    assigned to it by a coloring algorithm.
    
    Attributes:
      bucket (Node): a reference to the bucket the Node occupies within
        the DEGREE data structure (see DEGREE for more details).
      color (int): the color of the node, assigned to it by a coloring
        algorithm.
      data (object): the pointer to the data that the Node is holding.
      flag (boolean): a flag that can be used in search algorithms to
        mark the node.
      head (Node): the pointer to the Node that comes before the Node
        on a linked list.
      nid (int): the Node ID, a value that is used to uniquely identify
        each Node inside a list.
      tail (Node): the pointer to the Node that comes after the Node
        on a linked list.
    """
    
    def __init__(
            self, nid, bucket=None, color=SENTINEL, data=None, 
            flag=False, head=None, tail=None):
        """Create a new node.
        
        Args:
          nid (int): the Node ID. It is used to uniquely identify a
            node inside a linked list.
          bucket (Node): the reference to the copy Node within some
            bucket inside a DEGREE data structure. Defaults to None.
          color (int): the color assigned to the node by a coloring
            algorithm. Defaults to the SENTINEL value
          data (object): the reference to the data that is contained
            within the node. Defaults to None.
          flag (boolean): a flag used to mark the node by search
            algorithms. Defaults to False.
          head (Node): the reference to the Node that is before the
            node on a linked list. Defaults to None.
          tail (Node): the reference to the Node that is after the
            node on a linked list. Defaults to None.
            
        Complexity: O(1)
        """
        self.nid = nid
        self.bucket = bucket
        self.color = color
        self.data = data    
        self.flag = flag    
        self.head = head
        self.tail = tail
    
    def __eq__(self, other):
        """Determine if the Node is equal to some other object.
        
        A Node is considered equal to other object if and only
        if the other object is also a Node instance, and if both
        Nodes' IDs are the same.
        
        Args:
          other (object): the object to test equality.
          
        Complexity: O(1)
          
        Returns:
          boolean: True if and only if 'other' is also a Node, and if
          its Node ID is equal to the Node's Node ID. False otherwise.
        """        
        if isinstance(other, Node):
            return other.nid == self.nid
            
        return False
    
    def __hash__(self):
        """Obtain a hash value for the Node.
        
        Since each Node ID uniquely identifies a node, the hash value
        is just the Node ID.
        
        Complexity: O(1)
        
        Returns:
          int: the Node ID.
        """
        return self.nid
    
    def __len__(self):
        """Determine the 'size' of the data that the Node is holding.
        
        If the data is a DoublyLinkedList, the number of elements in
        the list is returned (as the list represents the neighbors of
        the Node in a graph, and thus calling "len" is equal to
        determine the degree of a vertex in a GRAPH); if the data
        is any other object, or if the node holds no data, the SENTINEL
        value is returned instead.
        
        Complexity: O(1)
        
        Returns:
          int: an integer representing the "size" of the data the Node
            is holding.
        """
        if isinstance(self.data, DoublyLinkedList):
            return len(self.data.elements)        
        else:
            return SENTINEL
    
    def __ne__(self, other):
        """Determine if the Node is not equal to some other object.
        
        A Node is considered not equal to other object if the other
        object is not a Node, or if the other object is an instance
        of Node with a different Node ID.
        
        Args:
          other (object): the object to test inequality.
          
        Complexity: O(1)
          
        Returns:
          boolean: False if and only if 'other' is also a Node and
          both Nodes have equal IDs. True otherwise.
        """
        if isinstance(other, Node):
            return other.nid != self.nid
            
        return True

    def __repr__(self):
        """Construct the official representation of the Node.
        
        Complexity O(deg(v)), where deg(v) is the number of neighbors
          of the node in a graph.
        
        Returns:
            string: a JSON string representing the Node.
        """
        if isinstance(self.data, DoublyLinkedList):
            neighbors = [str(v.nid) for v in self.data]
        else:
            neighbors = []
            
        return '{{"vid":{0},"label":"{1}","neighbors":[{2}]}}'.format(
            str(self.nid),
            str(self.color),
            ",".join(neighbors)
        )

    def __str__(self):
        """Construct a readable representation of the Node.
        
        Complexity: O(1)
        
        Returns:
          string: a representation of the Node.
        """
        if isinstance(self.data, Node):
            str_data = str(self.data.nid)
        elif isinstance(self.data, DoublyLinkedList):
            str_data = " adjacency list"
        else:
            str_data = str(self.data)
        
        if self.color == SENTINEL:
            if self.flag:
                str_color = "( None )"
            else:
                str_color = "[ None ]"
        else:
            if self.flag:
                str_color = "( {0} )".format(str(self.color))
            else:
                str_color = "[ {0} ]".format(str(self.color))
        
        return "[ ^ {0} | ( {1} ) --> {2}  | {3} | {4} v ]".format(
          str(self.head.nid) if self.head is not None else "GND",
          str(self.nid),
          str_data,
          str_color,
          str(self.tail.nid) if self.tail is not None else "GND"
        )


class DoublyLinkedList(object):
    """Implement a doubly linked list.
    
    Doubly linked lists are linked data structures that consists of a
    set of sequentially linked records called 'nodes'. Each node
    contains two fields, called 'links', that are references to the
    previous and to the next node in the sequence of nodes. The
    beginning and ending nodes' head and tail links, respectively, 
    point to some kind of terminator, typically a sentinel node or a
    null value.
    
    You can picture a doubly linked list as a set of elephants standing
    in line. Each elephant in the line grabs the tail of the elephant 
    that is in front of it with its trunk, whilst its own tail is 
    grabbed by the elephant that is behind of it. Only the first 
    elephant has its trunk free, and also only the last elephant has 
    its tail free.
    
    Nodes within the DoublyLinkedList are kept inside a Python 
    dictionary, in order to increase efficiency in tasks such as
    indexing or checking existence. This does not modify the normal 
    behavior of a normal doubly linked list.
    
    Attributes:
      current (Node): a pointer to the Node that is being used right
        now. It is used to iterate over the list.
      elements (dict): the dictionary containing the nodes inside the
        list. It is used to increase efficiency in tasks such as
        indexing and checking existence.
      first (Node): the reference to the first Node on the list. The
        first Node's head should be the only one in the entire list to
        have the None value.
      last (Node): the reference to the last Node on the list. The last
        Node's tail should be the only one in the entire list to have
        the None value.
    """
    
    def __init__(self):
        """Create a new, empty doubly linked list.
        
        Complexity: O(1)
        """
        self.current = None
        self.elements = dict()
        self.first = None
        self.last = None
    
    def __contains__(self, element):
        """Determine if the given element is contained within the
        doubly linked list.
        
        Since a dictionary with the nodes in the linked list is keeped
        in order to maintain efficiency, to determine if the list 
        contains a given element is achieved through looking at the 
        dictionary, which is O(1), as opposed to the O(n) searching
        in a standard doubly linked list.
        
        Args:
          element (object): the object to test if is inside the list.
            It can be either a Node instance or an integer representing
            a Node Id.
        
        Complexity: O(1)
        
        Returns:
          boolean: True if and only if 'element' is a Node instance
            equal to some Node inside the list, or if 'element' is
            an integer equal to the node ID of some vertex inside
            the list. False otherwise.
        """
        if isinstance(element, Node):
            return element.nid in self.elements
        elif isinstance(element, int):
            return element in self.elements
        else:
            return False
    
    def __getitem__(self, nid):
        """Get the node within the list with the Node ID given.
        
        Since a dictionary of the nodes inside the list is keeped,
        indexing a specific node in the list just takes O(1) time.
        
        Args:
          nid (int): the node id of the desired Node.
          
        Complexity: O(1)
          
        Returns (Node): the reference of the Node with the given
          node id, or None if the linked list does not contain a
          Node with the specified node id.
        """
        if nid in self.elements:
            return self.elements[nid]
        else:
            return None
    
    def __iter__(self):
        """Prepare the list to be iterated.
        
        This methods changes the pointer for the current node to the
        first node in the list. Since a pointer to the first element
        is always kept, this method takes O(1) time.
        
        Complexity: O(1)
        
        Returns:
          DoublyLinkedList: the list itself.
        """
        self.current = self.first
        
        return self
    
    def __len__(self):
        """Determine the size of the DoublyLinkedList.
        
        The size of the list is the number of elements that is inside
        of it. Since the elements are keeped inside a dictionary, 
        checking the size of the list takes O(1) time, as opposed to
        the O(n) time of a regular doubly linked list.
        
        Complexity: O(1)
        
        Returns:
          int: an integer with the number of elements inside the list.
        """
        return len(self.elements)
    
    def __next__(self):
        """Move the pointer to the next element on the list.
        
        If the current pointer is None, then the end of the list was
        reached, and thus the iteration is stopped. Following the
        "head" and "tail" pointers is done in O(1), so this method
        takes O(1) time.
        
        Complexity: O(1)
        
        Returns:
          Node: the next element to use during an iteration of 
            the list.
        """
        if self.current is None:
            raise StopIteration
        elif self.current.tail is not None:
            self.current = self.current.tail
            
            return self.current.head
        else:
            self.current = self.current.tail
            
            return self.last
    
    def __str__(self):
        """Constructs a readable version of the doubly linked list
        
        The representation follows the internal structure of the list
        (that is, it follows the 'tails' of every node to get to the
        following node). Since all nodes are required to get the
        representation, the complexity of this method is O(n).
        
        Complexity: O(n)
        
        Returns:
          string: a representation of the list.
        """
        if self.is_empty():
            return " [ E m p t y   l i s t ] "
        
        nodes = []
        
        for vertex in self:
            nodes.append(str(vertex))
        
        return "\n".join(nodes)
    
    def append(self, node):
        """Add a node at the end of the doubly linked list.
        
        The vertex is also added to the vertex dictionary, to help
        maintain efficiency. Since a pointer to the last node is 
        always kept, adding a node to the end of the list just implies
        updating "head" and "tail" pointer, which is done in O(1), and
        so append a new node to the end of the list takes O(1) time.
        
        If a node with the Node ID of the given node is already present
        on the list, the new node is not added to the list again.
        
        Args:
          node (Node): the node to insert at the end of the list.
        
        Complexity: O(1)
          
        Returns:
          boolean: True if the node is inserted successfully. False
            otherwise.
        """
        if node.nid not in self.elements:
            # If list is empty, the new node becomes the first and last.
            if self.is_empty():
                self.first = node;
                self.last = node;
                
                self.first.head = None
                self.first.tail = None
            # Else it only becomes the last.
            else:
                node.head = self.last
                node.tail = None
                
                self.last.tail = node
                self.last = node
            
            # Adds the element to the dictionary
            self.elements[node.nid] = node
            
            return True
        else:
            return False
    
    def insert(self, value):
        """Inserts the given value as a new Node in the list.
        
        This methods is designed to maintain the Nodes of the list
        in a decreasing order (that is, the Node IDs of the elements
        in the list will be sorted in such way that every 'head' will
        have a Node ID higher than it's tail). This method requires
        o(n) to complete, since all Node IDs are checked in the worst
        case. If the order of the nodes is not important within the
        list, use 'append' instead, which takes O(1) time to complete.
        
        If a Node with the given Node ID already exists in the list,
        no changes are made.
        
        Args:
          value (int): the Node ID of the new node to be inserted in
            the doubly linked list.
            
        Complexity: O(n)
            
        Returns:
          boolean: True if and only if the new Node is inserted in its
            right place within the list. False otherwise.
        """
        # Check if node is not already in the list
        if value in self:
            return False
        
        # If list is empty, no need to check values
        if self.is_empty():
            return self.append(Node(value))
        
        # Check if the value is lower than the last node, 
        # for efficiency purposes
        if value < self.last.nid:
            return self.append(Node(value))
        
        self.current = self.first
        
        # Iterates over the list
        while self.current is not None:
            # Checks the values
            if value > self.current.nid:
                # New node is inserted at the beginning
                if self.current is self.first:
                    new_vertex = Node(value)
                    self.current.head = new_vertex
                    
                    new_vertex.tail = self.current
                    new_vertex.head = None
                    self.first = new_vertex
                    
                    self.elements[value] = new_vertex
                    
                    return True
                # New node is inserted in the middle of the list
                else:
                    new_vertex = Node(value)
                    
                    new_vertex.head = self.current.head
                    new_vertex.tail = self.current
                    
                    self.current.head.tail = new_vertex
                    self.current.head = new_vertex
                    
                    self.elements[value] = new_vertex
                    
                    return True
            
            self.current = self.current.tail
            
        # We shouldn't exit the cycle
        return False
                
    def is_empty(self):
        """Determines if the list is empty. 
        
        A doubly linked list is empty if and only if both its first
        and last elements are equal to None.
        
        Since pointers to the first and last elements of the list are
        always kept, checking if the list is empty takes O(1) time.
        
        Complexity: O(1)
        
        Returns:
          boolean: True if and only if both the first and last pointers
            of the list are equal to None. False otherwise.
        """
        return self.first is None and self.last is None
    
    def remove(self, nid):
        """Removes the Node with the Node ID given from the list.
        
        If no node inside the list has the node id specified, the
        list will remain unchanged. Since a dictionary with the 
        elements is kept, removing a node from the list takes O(1)
        time.
        
        Args:
          nid (int): the node to be deleted.
        
        Complexity: O(1)
        
        Returns:
          Node: the node with the node ID given, with the connections
            removed from the other nodes on the list, or None if the
            given node ID is not inside the list.
        """
        # Check if a node is to be deleted
        if nid is None:
            return None
        
        # Check if the node exists in the list
        if nid not in self.elements:
            return None
        
        # Removes the node from the list
        node = self.elements.pop(nid)
                
        # Checks if the node is the only one...
        if self.first == node and self.last == node:
            self.first = None
            self.last = None
            
            node.head = None
            node.tail = None
        # ...the first...
        elif self.first == node:
            node.tail.head = None
            self.first = node.tail            
            node.tail = None
        # ...the last...
        elif self.last == node:
            node.head.tail = None
            self.last = node.head
            node.head = None
        # ...or if it is on the middle  
        else:
            node.head.tail = node.tail
            node.tail.head = node.head    
            
            node.head = None
            node.tail = None
            
        return node

    def remove_first(self):
        """Removes the first Node on the list.
        
        Since a pointer to the first node is always kept, this method
        takes O(1) time to complete.
        
        Complexity: O(1)
        
        Returns:
          Node: The first Node on the list, or None if the list is 
            empty.
        """
        if not self.is_empty():
            node = self.elements.pop(self.first.nid)
            
            # Checks if the node is the only one
            if node.tail is not None:
                node.tail.head = None
                self.first = node.tail
                node.tail = None
            else:
                self.first = None
                self.last = None
                
            return node
            
        return None


class GRAPH(object):
    """Implements the GRAPH data structure as defined by Widgerson.
    
    GRAPH is used, as the name implies, to represent graphs. GRAPH has
    a doubly linked list for the vertices. Each vertex points to its
    adjacency list, which is also doubly linked. In addition if (u, w)
    is an edge of the graph, then w on u's list will point to u on w's 
    list and vice versa.
    
    Attributes:
      degrees (DEGREE): the data structure that contains the degrees of
        all vertices in the GRAPH.
      m (int): the number of vertices inside the GRAPH.
      n (int): the number of edges inside the GRAPH.
      vertices (DoublyLinkedList): the doubly linked list that contains
        the vertices of the GRAPH.
    """
    
    def __init__(self):
        """Create a new, empty GRAPH
        
        Complexity: O(1)
        """
        self.degrees = None
        self.m = 0
        self.n = 0
        self.vertices = DoublyLinkedList()

    def __deepcopy__(self, memo):
        """Create a deep copy of the GRAPH.
        
        The internal structure of the graph is preserved, however the
        Nodes and DoublyLinkedLists of the new GRAPH are completely 
        different to those of the original GRAPH. That is, after making
        a deep copy, two GRAPHS A and its copy B will contain the same 
        data, but modifying one will not affect the data of the other.
        
        Args:
          memo (dict): the dictionary of objects already copied during
            the copy process. It is automatically created and mantained
            by Python, so users need not to worry about it.
            
        Returns:
          GRAPH: A fully independient copy (a 'deep copy') of the
            GRAPH, with the same vertices and edges BUT in different
            data structures.
        """
        copy = GRAPH()
        
        for vertex in self.vertices:
            copy.add_vertex(vertex.nid)
            copy.vertices[vertex.nid].color = vertex.color
        
        # Create the edges of the copy
        for vertex in self.vertices:
            for neighbor in vertex.data:
                copy.add_edge(vertex.nid, neighbor.nid)
                
        if self.degrees is not None:
            copy.build_DEGREE()
            
        return copy

    def __repr__(self):
        """Create the official representation of the GRAPH.
        
        The string is in the JSON format, to make GRAPHS fully 
        compatible with the Java Graph Viewer Engine.
        
        Since all the GRAPH is on the representation, the complexity
        of this method is O(|V| + |E|).
        
        Complexity: O(|V| + |E|)
        
        Returns:
          string: a JSON representation of the GRAPH.
        """
        string_vertices = [repr(v) for v in self.vertices]
        
        string_edges = []
        
        for vertex in self.vertices:
            for neighbor in vertex.data:
                endA = vertex.nid
                endB = neighbor.nid
                
                # Since every edge is stored twice, we only added every
                # one of them the first time it appears.
                if endA < endB:
                    string_edges.append(
                      '{{"endpoints":[{0},{1}],"directed":false}}'.format(
                        str(endA - 1),
                        str(endB - 1)
                      )
                    )
                    
        return '{{"vertices":[{0}],"edges":[{1}]}}'.format(
          ",".join(string_vertices),
          ",".join(string_edges)
        )

    def __str__(self):
        """Create a readable representation of the GRAPH.
        
        Since all vertices and edges are needed to get the 
        representation, this method takes O(|V| + |E|) to complete.
        
        Complexity: O(|V| + |E|)
        
        Returns:
          string: a representation of the GRAPH.
        """
        adjacencies = []
        
        for vertex in self.vertices:
            adjacencies.append("Vertex: {0}\n{1}".format(
                str(vertex.nid),
                str(vertex.data)
              )
            )
            
        return "Vertices:\n{0}\nAdjacencies lists:\n{1}\n".format(
          str(self.vertices),
          "\n".join(adjacencies)
        )
    
    def add_edge(self, endA, endB):
        """Add a new edge to the GRAPH.
        
        The adjacency list of each vertex is updated with a copy of
        their new neighbor, both of which are mutually linked. Since 
        the vertices are kept in a dictionary, looking for the 
        adjacency list of each neighbor takes O(1). Also, adding new
        vertices to the adjacency list takes O(1), so the overall
        complexity of the method is O(1).
        
        If one (or both) of the endpoints specified is (are) not in
        the GRAPH, no changes are made.
        
        Args:
          endA (int): the first endpoint.
          endB (int): the second endpoint.
          
        Complexity: O(1)
          
        Returns:
          boolean: True if and only if the edge is added to the GRAPH
            successfully. False otherwise.
        """
        if endA in self.vertices and endB in self.vertices:
            # Create a copy of the vertices to store them in the
            # adjacency list.
            neighborA = Node(endA)
            neighborB = Node(endB)
            
            # Link mutually the two neighbors
            neighborA.data = neighborB
            neighborB.data = neighborA
            
            # Updates the adjacency list for both neighbors
            result = self.vertices[endA].data.append(neighborB)
            result = result and self.vertices[endB].data.append(neighborA)
            
            if result:
                self.n += 1
            
            return result
            
        return False
    
    def add_vertex(self, vid):
        """Add a new vertex to the GRAPH.
        
        If the vertex id already exists in the GRAPH, no changes are 
        made. Since the vertices are kept in a dictionary, checking if
        the given ID already exists takes O(1), and adding new nodes to
        the linked list also takes O(1) time, so the overall complexity
        of this method is O(1).
        
        Args:
          vid (int): the vertex ID of the new vertex.
          
        Complexity: O(1)
          
        Returns:
          boolean: True if and only if the vertex is added to the GRAPH
          successfully. False otherwise.
        """
        if vid not in self.vertices:
            new_vertex = Node(vid)
            new_vertex.data = DoublyLinkedList()            

            self.vertices.append(new_vertex)
            
            self.m += 1
            
            return True
            
        return False
    
    def build_DEGREE(self):
        """Builds the DEGREE data structure of the GRAPH.
        
        Building a DEGREE data structure involves iterating over
        all the vertices. Determine the bucket of a vertex can be
        done in O(1) time (since DEGREE uses DoublyLinkedList to
        store the buckets), but adding the vertex to a bucket takes
        O(|E|), so the overall complexity of building the DEGREE data
        structure is O(|V| + |E|).
        
        Complexity: O(|V| + |E|)
        """
        self.degrees = DEGREE()
        
        for vertex in self.vertices:
            self.degrees.add(vertex)
            
    def check_coloring(self):
        """Check that the GRAPH has a valid coloring.
        
        A coloring is valid if and only if no adjacent vertices share
        the same color. This method checks every vertex to check that
        their neighbor all have different colors. If two adjacent
        vertices with the same color are found, then a RuntimeError is
        raised.
        
        Since this method visits every vertex and check their adjacency
        lists, this method takes O(|V| * |V|) to complete.
        
        Complexity: O(|V| * |V|)
        
        Raises:
          RuntimeError: If two adjacent vertices share the same color.
        """
        for v in self.vertices:
            for neighbor in v.data:
                if v.color == self.vertices[neighbor.nid].color:
                    raise RuntimeError(
                      "INVALID COLORING: vertex {0} and vertex {1} share the color {2}".format(
                        v.nid, 
                        neighbor.nid,
                        v.color
                      )
                    )
                    
        print("Coloring is valid. No problems found.")
    
    def delete_edge(self, endA, endB):
        """Delete an edge from the GRAPH.
        
        If the edge indeed exists within the GRAPH, the adjacency
        lists for both endpoints will be updated. If the edge is
        not present within the GRAPH, no changes are made.
        
        Since the vertices are kept in a dictionary, and the adjacency
        lists are doubly linked lists, delete edges from the graph
        takes O(1) time.
        
        Args:
          endA (int): the vertex id of the first endpoint.
          endB (int): the vertex id of the second endpoint.
          
        Complexity: O(1)
          
        Returns:
          boolean: True if and only if the edge is deleted from the
            GRAPH. False otherwise.
        """
        if endA in self.vertices and endB in self.vertices:
            # Searches the adjacency lists
            listA = self.vertices[endA].data
            listB = self.vertices[endB].data
                        
            # Searches the nodes to be deleted 
            # (in case the edge is inverted)
            nodeA = listA[endB]
            nodeB = nodeA.data
                        
            # Deletes the edge
            result = (listA.remove(nodeA.nid) is not None)
            result = result and (listB.remove(nodeB.nid) is not None)
            
            if result:
                self.n -= 1
            
            return result
            
        return False
    
    def delete_vertex(self, vid):
        """Delete a vertex from the GRAPH.
        
        The adjacency list of the vertex's neighbors is NOT
        updated to reflect the remotion of the vertex. This is made
        in order to preserve the lineal complexity of the data 
        structure, as defined by Widgerson in his paper. This way,
        deleting a vertex is done in O(1) time.
        
        If no vertex with the vertex ID given is in the list, no
        changes are made.
        
        Args:
          vid (int): the vertex ID of the vertex to be removed.
        
        Complexity: O(1)
          
        Returns:
          Node: the node deleted from the GRAPH, with its adjacency
            list unchanged, or None if the vertex ID given does not
            belong to any vertex in the GRAPH.
        """
        if vid not in self.vertices:
            return None
        else:
            self.m -= 1
            
            return self.vertices.remove(vid)
            
    def get_colors_used(self):
        """Get the amount of different colors used in the graph.
        
        Complexity: O(|V|)
        
        Returns:
          int: the number of different colors used to color the graph.
        """
        colors = set()
        
        for v in self.vertices:
            colors.add(v.color)
            
        return len(v)
            
    def get_max_degree(self):
        """Get the max degree currently found in the GRAPH.
        
        The max degree is directly obtained from the DEGREE data
        structure associated with the GRAPH. If the DEGREE data
        structure is None, then it's created as needed.
        
        If the DEGREE data structure has not been created, this method
        takes O(|V| + |E|) to complete; if it has been created, it only
        takes O(|E|) time.
        
        Complexity: O(|V| + |E|) if DEGREE hasn't been created, 
          O(|E|) otherwise.
        
        Returns:
          int: the maximum degree found in the GRAPH.
        """
        if self.degrees is None:
            self.build_DEGREE()
            
        current_degree = self.degrees.buckets.first
        
        while current_degree.data.is_empty():
            current_degree = current_degree.tail
            
        self.degrees.max_degree = current_degree.nid
            
        return self.degrees.max_degree
        
    def get_max_degree_vertex(self):
        """Get the reference for a vertex with maximum degree in the
        GRAPH.
        
        The max degree is directly obtained from the DEGREE data
        structure associated with the GRAPH. If the DEGREE data
        structure is None, then it's created as needed.
        
        If the DEGREE data structure has not been created, this method
        takes O(|V| + |E|) to complete; if it has been created, it only
        takes O(|E|) time.
        
        Complexity: O(|V| + |E|) if DEGREE hasn't been created,
          O(|E|) otherwise.
        
        Returns:
          Node: A node with maximum degree inside the GRAPH.
        """
        if self.degrees is None:
            self.build_DEGREE()
        
        # Gets the copy of a vertex with maximum degree
        vertex = None
        current_bucket = self.degrees.buckets.first
        
        # Checks if the vertex is not None
        while vertex is None:
            vertex = current_bucket.data.first
            self.degrees.max_degree = current_bucket.nid
            current_bucket = current_bucket.tail            
        
        # Return the original vertex from the graph
        return vertex.data
        
    def get_min_degree(self):
        """Get the min degree currently found in the GRAPH.
        
        The min degree is directly obtained from the DEGREE data
        structure associated with the GRAPH. If the DEGREE data
        structure is None, then it's created as needed.
        
        If the DEGREE data structure has not been created, this method
        takes O(|V| + |E|) to complete; if it has been created, it only
        takes O(|E|) time.
        
        Complexity: O(|V| + |E|) if DEGREE hasn't been created, 
          O(|E|) otherwise.
        
        Returns:
          int: the minimum degree found in the GRAPH.
        """
        if self.degrees is None:
            self.build_DEGREE()
            
        current_degree = self.degrees.buckets.last
        
        while current_degree.data.is_empty():
            current_degree = current_degree.head
            
        self.degrees.min_degree = current_degree.nid
            
        return self.degrees.min_degree
        
    def get_min_degree_vertex(self):
        """Get the reference for a vertex with minimum degree in the
        GRAPH.
        
        The min degree is directly obtained from the DEGREE data
        structure associated with the GRAPH. If the DEGREE data
        structure is None, then it's created as needed.
        
        If the DEGREE data structure has not been created, this method
        takes O(|V| + |E|) to complete; if it has been created, it only
        takes O(|E|) time.
        
        Complexity: O(|V| + |E|) if DEGREE hasn't been created,
          O(|E|) otherwise.
        
        Returns:
          Node: A node with minimum degree inside the GRAPH.
        """
        if self.degrees is None:
            self.build_DEGREE()
        
        # Gets the copy of a vertex with minimum degree
        vertex = None
        current_bucket = self.degrees.buckets.last
        
        # Checks that the vertex is not None
        while vertex is None:
            vertex = current_bucket.data.first
            self.degrees.min_degree = current_bucket.nid
            current_bucket = current_bucket.head
        
        # Return the original vertex from the graph
        return vertex.data
    
    def get_random_vertex(self, proposal=0, exp=1):
        """Get the reference to a vertex randomly choosed from the 
        GRAPH.
                
        Different proposals are given to choose the vertex in a 
        'random' way. Since every proposal is quite different to each
        other, this method has no complexity measured 'per se'. Please
        refer to the documentation of the proposals to get more 
        information about the metodology used to choose the vertices
        inside every proposal. 
        
        Args:
          proposal (int): tells the method which of the proposals
            to use to select a vertex 'randomly'. If not given, a
            vertex is randomly choosed with uniform probability.
            Defaults to 0 (zero).
          exp (float): the exponent to which the formula for choosing
            random vertices will be raised. Defaults to 1.

        Complexity: Undefined. Each proposal defines its own 
          complexity.
        
        Returns: 
          Node: A node randomly choosed from the GRAPH.
        """
        if self.degrees is None:
            self.build_DEGREE()
            
        if proposal == 1:
            return self.proposal_1()
        elif proposal == 2:
            return self.proposal_2()
        elif proposal == 3:
            return self.proposal_3()
        elif proposal == 4:
            return self.proposal_4()
        elif proposal == 5:
            return self.proposal_5()
        elif proposal == 6:
            return self.proposal_6()
        elif proposal == 7:
            return self.proposal_7()
        elif proposal == 8:
            return self.proposal_8(exp)
        elif proposal == 9:
            return self.proposal_9()
        elif proposal == 10:
            return self.proposal_10()
        elif proposal == 11:
            return self.proposal_11()
        elif proposal == 12:
            return self.proposal_12()
        elif proposal == 13:
            return self.proposal_13()
        elif proposal == 14:
            return self.proposal_14()
        elif proposal == 15:
            return self.proposal_15()
        elif proposal == 16:
            return self.proposal_16()
        elif proposal == 17:
            return self.proposal_17()
        elif proposal == 18:
            return self.proposal_18()
        elif proposal == 19:
            return self.proposal_19()
        elif proposal == 20:
            return self.proposal_20()
        elif proposal == 21:
            return self.proposal_21()
        elif proposal == 22:
            return self.proposal_22()
        elif proposal == 23:
            return self.proposal_23()
        elif proposal == 24:
            return self.proposal_24()
        elif proposal == 25:
            return self.proposal_25()
        elif proposal == 26:
            return self.proposal_26()
        elif proposal == 27:
            return self.proposal_27()
        elif proposal == 28:
            return self.proposal_28()
        elif proposal == 29:
            return self.proposal_29()
        elif proposal == 30:
            return self.proposal_30(exp)
        elif proposal == 31:
            return self.proposal_31()
        elif proposal == 32:
            return self.proposal_32()
        elif proposal == 33:
            return self.proposal_33()
        elif proposal == 34:
            return self.proposal_34()
        elif proposal == 35:
            return self.proposal_35()
        elif proposal == 36:
            return self.proposal_36()
        else:
            candidates = list(self.vertices.elements.keys())
            return self.vertices[random.choice(candidates)]
        
    def is_valid(self, nid, color):
        """Check if the Node can be assigned with the given color.
        
        This method checks the adjacency list of the Node, which takes
        O(deg(Node) to complete. Since a vertex can have at most 
        (|V| - 1) neighbors, this method takes O(|V|) time to complete.
        
        Args:
          nid (int): the Node ID of the node to check
          color (int): the color to check
          
        Complexity: O(|V|)
          
        Returns:
          boolean: True if and only if no node in the Node's adjacency
            list has the given color, and thus is safe to assign the 
            color to the Node. False otherwise.
        """
        vertex = self.vertices[nid]
        
        for neighbor in vertex.data:
            if color == self.vertices[neighbor.nid].color:
                return False
                
        return True
    
    def print_colors(self):
        """Print the colors assigned to the vertices of the GRAPH.
        
        Since all nodes are checked, this method takes O(|V|) to 
        complete.
        
        Complexity: O(|V|)
        """
        for vertex in self.vertices:
            print("( {0} ) --> {1}".format(vertex.nid, vertex.color))
    
    def proposal_1(self):
        """Implement the Proposal 1 for getting a random vertex from
        the GRAPH.
        
        This proposal visits every bucket (until a vertex is choosed),
        multiplies the degree of the bucket by the number of vertices
        inside of it, and then divides this result by twice the number
        of edges in the GRAPH: this value is then compared to a 
        uniformly distributed pseudo-random number to determine if the
        first vertex in that bucket is choosed or not.
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Since this method is based on pseudo-random numbers, its 
        complexity cannot be guaranteed, but it is O(|buckets|) most of
        the time, where |buckets| is the number of buckets in the 
        GRAPH's DEGREE data structure.
        
        Complexity: Approximately O(|buckets|)
        
        Returns
          Node: The reference to the first node of a bucket randomly
           choosed from the GRAPH's DEGREE data structure, with 
           probability proportional to the size of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        
        while choosed is None:
            p = (bucket.nid * len(bucket)) / (2 * self.n)
            
            if random.uniform(0, 1) < p:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
                
            if bucket is None:
                bucket = self.degrees.buckets.first
                
        return choosed.data
        
    def proposal_2(self):
        """Implement the Proposal 2 for getting a random vertex from
        the GRAPH.
        
        This proposal visits every bucket (until a vertex is choosed),
        multiplies the degree of the bucket by the number of vertices 
        inside of it, and then divides this result by twice the number
        of edges in the GRAPH: this value is then compared to a 
        uniformly distributed pseudo-random number to determine if a
        random vertex in that bucket is choosed or not.
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Since this method is based on pseudo-random numbers, its 
        complexity cannot be guaranteed, but it is O(|buckets|) most of
        the time, where |buckets| is the number of buckets in the 
        GRAPH's DEGREE data structure.
        
        Complexity: Approximately O(|buckets|)
        
        Returns
          Node: The reference to a random node of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with
            probability proportional to the size of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        
        while choosed is None:
            p = (bucket.nid * len(bucket)) / (2 * self.n)
          
            if random.uniform(0, 1) < p:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
                
            if bucket is None:
                bucket = self.degrees.buckets.first
            
        return choosed.data
        
    def proposal_3(self):
        """Implement the Proposal 3 for getting a random vertex from
        the GRAPH.
        
        This proposal visits every bucket (until a vertex is choosed),
        multiplies the degree of the bucket by the number of vertices
        inside of it, and then divides this result by twice the number
        of edges in the GRAPH: this value is then compared to a 
        uniformly distributed pseudo-random number to determine if the
        first vertex in that bucket is choosed or not.
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Since this method is based on pseudo-random numbers, its 
        complexity cannot be guaranteed, but it is O(|buckets|) most of
        the time, where |buckets| is the number of buckets in the 
        GRAPH's DEGREE data structure.
        
        Complexity: Approximately O(|buckets|)
        
        Returns:
          Node: The reference to the first node of a bucket randomly
          choosed from the GRAPH's DEGREE data structure, with 
          probability proportional to the size of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        
        while choosed is None:
            p = (bucket.nid * len(bucket)) / (2 * self.n)
            
            if random.uniform(0, 1) < p:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
            if bucket is None:
                bucket = self.degrees.buckets.last
                
        return choosed.data
    
    def proposal_4(self):
        """Implement the Proposal 4 for getting a random vertex from
        the GRAPH.
        
        This proposal visits every bucket (until a vertex is choosed),
        multiplies the degree of the bucket by the number of vertices 
        inside of it, and then divides this result by twice the number
        of edges in the GRAPH: this value is then compared to a
        uniformly distributed pseudo-random number to determine if a
        random vertex in that bucket is choosed or not.
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Since this method is based on pseudo-random numbers, its 
        complexity cannot be guaranteed, but it is O(|buckets|) most of
        the time, where |buckets| is the number of buckets in the
        GRAPH's DEGREE data structure.
        
        Complexity: Approximately O(|buckets|)
        
        Returns:
          Node: The reference to a random node of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        
        while choosed is None:
            p = (bucket.nid * len(bucket)) / (2 * self.n)
            t = random.uniform(0, 1)
            
            if t < p:
            #if random.uniform(0, 1) < p:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
                
            if bucket is None:
                bucket = self.degrees.buckets.last
                
        return choosed.data
    
    def proposal_5(self):
        """Implement the Proposal 5 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4 
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        higher degrees have higher probabilities of being choosed than
        buckets of smaller degrees. Also, when this method reaches the
        first bucket (the 'max degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is 
        O(|buckets|).
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
        return choosed.data
        
    def proposal_6(self):
        """Implement the Proposal 6 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the 
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        higher degrees have higher probabilities of being choosed than
        buckets of smaller degrees. Also, when this method reaches the
        first bucket (the 'max degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is 
        O(|buckets|).
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if not bucket.data.is_empty() and random.uniform(0, 1) < summa:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
        
        return choosed.data
        
    def proposal_7(self):
        """Implement the Proposal 7 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        higher degrees have higher probabilities of being choosed than
        buckets of smaller degrees. Also, when this method reaches the
        first bucket (the 'max degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
          choosed from the GRAPH's DEGREE data structure, with
          probability proportional to the size of the bucket AND the
          degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if throw < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
        return choosed.data
        
    def proposal_8(self, exp=1):
        """Implement the Proposal 8 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        higher degrees have higher probabilities of being choosed than
        buckets of smaller degrees. Also, when this method reaches the
        first bucket (the 'max degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in increasing order, and never
        selects vertices of degree 0.
        
        Args:
          exp (float): the exponent to which the formula for choosing
            random vertices will be raised to. Defaults to 1.
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += ( (bucket.nid * len(bucket)) / (2 * self.n) ) ** exp
            
            if throw < summa:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
                
            if bucket is None:
                bucket = self.degrees.buckets.last
                
        return choosed.data
        
    def proposal_9(self):
        """Implement the Proposal 9 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4 
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        smaller degrees have higher probabilities of being choosed than
        buckets of higher degrees. Also, when this method reaches the
        last bucket (the 'min degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed
        to be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
                
        return choosed.data
        
    def proposal_10(self):
        """Implement the Proposal 10 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of 
        smaller degrees have higher probabilities of being choosed than
        buckets of higher degrees. Also, when this method reaches the
        last bucket (the 'min degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        the method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if random.uniform(0, 1) < summa and not bucket.data.is_empty():
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
        
        return choosed.data
        
    def proposal_11(self):
        """Implement the Proposal 11 for getting a random vertex from 
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        smaller degrees have higher probabilities of being choosed than
        buckets of higher degrees. Also, when this method reaches the
        last bucket (the 'min degree' bucket) the probability of
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        this method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with
            probability inversely proportional to the size of the
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if throw < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
                
        return choosed.data
        
    def proposal_12(self):
        """Implement the Proposal 12 for getting a random vertex from
        the GRAPH.
        
        This proposal follows a similar approach as the first 4
        proposals, using the size of a bucket to compute the
        probability of choosing it. However, this proposal accumulates
        the probabilities of previous buckets: this way, buckets of
        smaller degrees have higher probabilities of being choosed than
        buckets of higher degrees. Also, when this method reaches the
        last bucket (the 'min degree' bucket) the probability of 
        choosing a bucket is 1, and therefore a vertex is guaranteed to
        be choosed, which results in an increased performance (since
        this method only visits the buckets once, as opposed to the
        first 4 proposals, where buckets may be visited more than once
        each). Thanks to this, the complexity of this method is
        O(|buckets|).
        
        This method visits the buckets in decreasing order, and never
        selects vertices of degree 0.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with
            probability inversely proportional to the size of the
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += (bucket.nid * len(bucket)) / (2 * self.n)
            
            if throw < summa:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
                
        return choosed.data
    
    def proposal_13(self):
        """Implement the Proposal 13 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 5, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it.
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of higher degrees have 
        higher probabilities of being choosed than buckets of smaller
        degrees. Also, when this method reaches the first bucket (the
        'max degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in increasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
        return choosed.data
        
    def proposal_14(self):
        """Implement the Proposal 14 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 6, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it.
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of higher degrees have 
        higher probabilities of being choosed than buckets of smaller
        degrees. Also, when this method reaches the first bucket (the
        'max degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in increasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if random.uniform(0, 1) < summa and not bucket.data.is_empty():
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
                
        return choosed.data
        
    def proposal_15(self):
        """Implement the Proposal 15 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 7, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it.
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of higher degrees have 
        higher probabilities of being choosed than buckets of smaller
        degrees. Also, when this method reaches the first bucket (the
        'max degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in increasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if throw < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
        return choosed.data
    
    def proposal_16(self):
        """Implement the Proposal 16 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 8, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it.
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of higher degrees have 
        higher probabilities of being choosed than buckets of smaller
        degrees. Also, when this method reaches the first bucket (the
        'max degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in increasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability proportional to the size of the bucket AND the
            degree of the bucket.
        """
        bucket = self.degrees.buckets.last
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if throw < summa:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
                
        return choosed.data
        
    def proposal_17(self):
        """Implement the Proposal 17 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 9, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it. 
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of smaller degrees have
        higher probabilities of being choosed than buckets of higher
        degrees. Also, when this method reaches the last bucket (the
        'min degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in decreasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
        
        return choosed.data
    
    def proposal_18(self):
        """Implement the Proposal 18 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 10, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it. 
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of smaller degrees have
        higher probabilities of being choosed than buckets of higher
        degrees. Also, when this method reaches the last bucket (the
        'min degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in decreasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if random.uniform(0, 1) < summa and not bucket.data.is_empty():
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
                
        return choosed.data
        
    def proposal_19(self):
        """Implement the Proposal 19 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 11, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it. 
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of smaller degrees have
        higher probabilities of being choosed than buckets of higher
        degrees. Also, when this method reaches the last bucket (the
        'min degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in decreasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to the first vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if throw < summa:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
                
        return choosed.data
        
    def proposal_20(self):
        """Implement the Proposal 20 for getting a random vertex from
        the GRAPH.
        
        This proposal is identical to Proposal 12, only modifying the
        probabilities to allow vertices of degree 0 to be choosed. It
        follows a similar approach as the first 4 proposals, using the
        size of a bucket to compute the probability of choosing it. 
        However, this proposal accumulates the probabilities of
        previous buckets: this way, buckets of smaller degrees have
        higher probabilities of being choosed than buckets of higher
        degrees. Also, when this method reaches the last bucket (the
        'min degree' bucket) the probability of choosing a bucket is 1,
        and therefore a vertex is guaranteed to be choosed, which
        results in an increased performance (since the method only
        visits the buckets once, as opposed to the first 4 proposals,
        where buckets may be visited more than once each). Thanks to
        this, the complexity of this method is O(|buckets|).
        
        This method visits the buckets in decreasing order, and allows
        vertices of degree 0 to be choosed.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a random vertex of a bucket randomly
            choosed from the GRAPH's DEGREE data structure, with 
            probability inversely proportional to the size of the 
            bucket AND the degree of the bucket.
        """
        bucket = self.degrees.buckets.first
        choosed = None
        summa = 0
        throw = random.uniform(0, 1)
        
        while choosed is None:
            summa += ((bucket.nid + 1) * len(bucket)) / (self.m + 2 * self.n)
            
            if throw < summa:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
                
        return choosed.data
        
    def proposal_21(self):
        """Implement the Proposal 21 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by the
        maximum degree occurring in the graph as the probability to
        choose a given vertex. As opposed to the first 20 proposals,
        this proposal follows a 'vertex-oriented' approach, instead of
        a 'bucket-oriented' approach.
        
        This method visits vertices as they are stored in the GRAPH,
        and never selects vertices of degree 0. Since this method 
        depends on pseudo-random numbers, its complexity cannot be
        guaranteed, however its complexity is O(|V|) most of the time.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's 
            degree.
        """
        choosed = None
        max_degree = self.get_max_degree()
        
        while choosed is None:
            for vertex in self.vertices:
                p = len(vertex) / max_degree
                
                if random.uniform(0, 1) < p:
                    choosed = vertex
                    break
        
        return choosed
        
    def proposal_22(self):
        """Implement the Proposal 22 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by the
        maximum degree occurring in the graph as the probability to
        choose a given vertex. As opposed to the first 20 proposals,
        this proposal follows a 'vertex-oriented' approach, instead of
        a 'bucket-oriented' approach.
        
        This method visits vertices as they are stored in the GRAPH,
        and never selects vertices of degree 0. Since this method 
        depends on pseudo-random numbers, its complexity cannot be
        guaranteed, however its complexity is O(|V|) most of the time.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        max_degree = self.get_max_degree()
        
        while choosed is None:
            throw = random.uniform(0, 1)
            
            for vertex in self.vertices:
                p = len(vertex) / max_degree
                
                if throw < p:
                    choosed = vertex
                    break
                    
        return choosed
        
    def proposal_23(self):
        """Implement the Proposal 23 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by the
        maximum degree occurring in the graph as the probability to
        choose a given vertex. As opposed to the first 20 proposals,
        this proposal follows a 'vertex-oriented' approach, instead of
        a 'bucket-oriented' approach.
        
        This method visits vertices as they are stored in the GRAPH,
        and allows vertices of degree 0 to be selected. Since this method 
        depends on pseudo-random numbers, its complexity cannot be
        guaranteed, however its complexity is O(|V|) most of the time.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        max_degree = self.get_max_degree() + 1
        
        while choosed is None:
            for vertex in self.vertices:
                p = (len(vertex) + 1) / max_degree
                
                if random.uniform(0, 1) < p:
                    choosed = vertex
                    break
                    
        return choosed
        
    def proposal_24(self):
        """Implement the Proposal 24 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by the
        maximum degree occurring in the graph as the probability to
        choose a given vertex. As opposed to the first 20 proposals,
        this proposal follows a 'vertex-oriented' approach, instead of
        a 'bucket-oriented' approach.
        
        This method visits vertices as they are stored in the GRAPH,
        and allows vertices of degree 0 to be selected. Since this
        method depends on pseudo-random numbers, its complexity cannot
        be guaranteed, however its complexity is O(|V|) most of the
        time.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        max_degree = self.get_max_degree() + 1
        
        while choosed is None:
            throw = random.uniform(0, 1)
            
            for vertex in self.vertices:
                p = (len(vertex) + 1) / max_degree
                
                if throw < p:
                    choosed = vertex
                    break
        
        return choosed
        
    def proposal_25(self):
        """Implement the Proposal 25 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by twice the
        number of edges in the graph. However, probabilities of 
        previous vertices are accumulated, making that later vertices
        have higher posibilities of being choosed than the first ones.
        As opposed to the first 20 proposals, this proposal follows a
        'vertex-oriented' approach, instead of a 'bucket-oriented'
        approach.
        
        This method first randomly shuffles the vertices, visit them in
        that sorted order, and allows some vertices of degree 0 to be
        selected. Since the probabilities add to 1 when the last vertex
        is reached, this method's complexity is O(|V|).
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        summa = 0
        verts = list(self.vertices.elements.keys())
        random.shuffle(verts)
        
        for index in verts:
            summa += len(self.vertices[index]) / (2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = self.vertices[index]
                break
                
        return choosed
        
    def proposal_26(self):
        """Implement the Proposal 26 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by twice the
        number of edges in the graph. However, the probabilities of
        previous vertices are accumulated, making that later vertices
        have higher posibilities of being choosed than the first ones.
        As opposed to the first 20 proposals, this proposal follows a
        'vertex-oriented' approach, instead of a 'bucket-oriented'
        approach.
        
        This method first randomly shuffles the vertices, visit them in
        that sorted order, and allows some vertices of degree 0 to be
        selected. Since the probabilities add to 1 when the last vertex
        is reached, this method's complexity is O(|V|).
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        summa = 0
        verts = list(self.vertices.elements.keys())
        random.shuffle(verts)
        throw = random.uniform(0, 1)
        
        for index in verts:
            summa += len(self.vertices[index]) / (2 * self.n)
            
            if throw < summa:
                choosed = self.vertices[index]
                break
            
        return choosed
        
    def proposal_27(self):
        """Implement the Proposal 27 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by twice the
        number of edges in the graph. However, the probabilities of
        previous vertices are accumulated, making that later vertices
        have higher posibilities of being choosed than the first ones.
        As opposed to the first 20 proposals, this proposal follows a
        'vertex-oriented' approach, instead of a 'bucket-oriented'
        approach.
        
        This method first randomly shuffles the vertices, visit them in
        that sorted order, and allows all vertices of degree 0 to be
        selected. Since the probabilities add to 1 when the last vertex
        is reached, this method's complexity is O(|V|).
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        summa = 0
        verts = list(self.vertices.elements.keys())
        random.shuffle(verts)
        
        for index in verts:
            summa += (len(self.vertices[index]) + 1) / (self.m + 2 * self.n)
            
            if random.uniform(0, 1) < summa:
                choosed = self.vertices[index]
                break
                
        return choosed
        
    def proposal_28(self):
        """Implement the Proposal 28 for getting a random vertex from
        the GRAPH.
        
        This proposal uses the degree of a vertex divided by twice the
        number of edges in the graph. However, the probabilities of
        previous vertices are accumulated, making that later vertices
        have higher posibilities of being choosed than the first ones.
        As opposed to the first 20 proposals, this proposal follows a
        'vertex-oriented' approach, instead of a 'bucket-oriented'
        approach.
        
        This method first randomly shuffles the vertices, visit them
        in that sorted order, and allows all vertices of degree 0 to be
        selected. Since the probabilities add to 1 when the last vertex
        is reached, this method's complexity uis O(|V|).
        
        Complexity: O(|V|)
        
        Returns: 
          Node: the reference to a vertex randomly choosed from the
            GRAPH, with probability proportional to the vertex's
            degree.
        """
        choosed = None
        summa = 0
        verts = list(self.vertices.elements.keys())
        random.shuffle(verts)
        throw = random.uniform(0, 1)
        
        for index in verts:
            summa += (len(self.vertices[index]) + 1) / (self.m + 2 * self.n)
            
            if throw < summa:
                choosed = self.vertices[index]
                break
        
        return choosed

    def proposal_29(self):
        """Implement the Proposal 29 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high
        degree. This proposal uses the inverse of the size of a bucket
        plus 1 as the probability of choosing the first vertex in said
        bucket.
        
        This proposal visits the buckets in order (from higher degree
        to smaller degree), and always choose zero-degree vertices
        when reached.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        bucket = self.degrees.buckets.first
        
        while choosed is None:
            p = 1.0 / (bucket.nid + 1)
            
            if not bucket.data.is_empty() and random.uniform(0, 1) < p:
                choosed = bucket.data.first
            else:
                bucket = bucket.tail
                
            if bucket is None:
                bucket = self.degrees.buckets.first
                
        return choosed.data
        
    def proposal_30(self, exp=1):
        """Implement the Proposal 30 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the size of a bucket
        plus 1 as the probability of choosing a random vertex in said
        bucket.
        
        This proposal visits the buckets in order (from higher degree
        to smaller degree), and always choose zero-degree vertices when
        reached.
        
        Args:
          exp (float): the exponent to which the formula for choosing
            random vertices will be raised to. Defaults to 1.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        bucket = self.degrees.buckets.first
        
        while choosed is None:
            p = ( 1.0 / (bucket.nid + 1) ) ** exp
            
            if not bucket.data.is_empty() and random.uniform(0, 1) < p:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.tail
                
            if bucket is None:
                bucket = self.degrees.buckets.first
                
        return choosed.data
    
    def proposal_31(self):
        """Implement the Proposal 31 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the size of a bucket
        plus 1 as the probability of choosing the first vertex in said
        bucket.
        
        This proposal visits the buckets in reverse order (from smaller
        degree to higher degree), and always choose zero-degree
        vertices when reached.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        bucket = self.degrees.buckets.last
        
        while choosed is None:
            p = 1.0 / (bucket.nid + 1)
            
            if not bucket.data.is_empty() and random.uniform(0, 1) < p:
                choosed = bucket.data.first
            else:
                bucket = bucket.head
                
            if bucket is None:
                bucket = self.degrees.buckets.last
                
        return choosed.data
        
    def proposal_32(self):
        """Implement the Proposal 32 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high
        degree. This proposal uses the inverse of the size of a bucket
        plus 1 as the probability of choosing a random vertex in said
        bucket.
        
        This proposal visits the buckets in reverse order (from smaller
        degree to higher degree), and always choose zero-degree
        vertices when reached.
        
        Complexity: O(|buckets|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        bucket = self.degrees.buckets.last
        
        while choosed is None:
            p = 1.0 / (bucket.nid + 1)
            
            if not bucket.data.is_empty() and random.uniform(0, 1) < p:
                candidates = list(bucket.data.elements.keys())
                choosed = bucket.data.elements[random.choice(candidates)]
            else:
                bucket = bucket.head
                
            if bucket is None:
                bucket = self.degrees.buckets.last
                
        return choosed.data
    
    def proposal_33(self):
        """Implement the Proposal 33 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the degree of a 
        vertex plus 1 as the probability of choosing said vertex.
        
        This proposal visits the vertices in the order in which they
        are stored inside the GRAPH, and always choose zero-degree
        vertices when reached.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        
        while choosed is None:
            for vertex in self.vertices:
                p = 1.0 / (len(vertex) + 1)
                
                if random.uniform(0, 1) < p:
                    choosed = vertex
                    break
                
        return choosed
    
    def proposal_34(self):
        """Implement the Proposal 34 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the degree of a 
        vertex plus 1 as the probability of choosing said vertex.
        
        This proposals visits the vertices in the order in which they
        are stored inside the GRAPH, uses a fixed value called 'throw'
        as the value that decides if a vertex is choosed, and always 
        choose zero-degree vertices when reached.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        
        while choosed is None:
            throw = random.uniform(0, 1)
            for vertex in self.vertices:
                p = 1.0 / (len(vertex) + 1)
                
                if throw < p:
                    choosed = vertex
                    break
                    
        return choosed
    
    def proposal_35(self):
        """Implement the Proposal 35 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the degree of a 
        vertex plus 1 as the probability of choosing said vertex.
        
        This proposal visits the vertices in random order, and
        always choose zero-degree vertices when reached.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the reference to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        indexes = list(self.vertices.elements.keys())
        random.shuffle(indexes)
        
        while choosed is None:
            for vid in indexes:
                p = 1.0 / (len(self.vertices[vid]) + 1)
            
                if random.uniform(0, 1) < p:
                    choosed = self.vertices[vid]
                    break
                
        return choosed
        
    def proposal_36(self):
        """Implement the Proposal 36 for getting a random vertex from
        the GRAPH.
        
        This proposal is designed to give vertices of small degree a
        higher probability of being choosed than vertices of high 
        degree. This proposal uses the inverse of the degree of a 
        vertex plus 1 as the probability of choosing said vertex.
        
        This proposal visits the vertices in random order, uses a fixed
        value called 'throw' as the value that decides if a vertex is
        choosed, and always choose zero-degree vertices when reached.
        
        Complexity: O(|V|)
        
        Returns:
          Node: the refence to a vertex randomly choosed from the
            GRAPH.
        """
        choosed = None
        indexes = list(self.vertices.elements.keys())
        random.shuffle(indexes)
        
        while choosed is None:
            throw = random.uniform(0, 1)
            for vid in indexes:
                p = 1.0 / (len(self.vertices[vid]) + 1)
                
                if throw < p:
                    choosed = self.vertices[vid]
                    break
                    
        return choosed
    
    def set_seed(self, seed):
        """Set the value of the seed for the pseudo-random number 
        generator.
        
        Args:
          seed (int): the seed for the generator.
          
        Complexity: O(1)
        """
        random.seed(seed)
    
    def subgraph(self, vertex):
        """Creates an induced subgraph from the neighborhood of the
        given vertex.
        
        All vertices in the neighborhood of the given vertices are
        first removed from the graph (with their adjacency lists
        complete). Then, all the non-remaining vertices on the new
        subgraph are deleted from the adjacency lists in both graphs
        (the original graph and the subgraph). Since the subgraph 
        contains the neighborhood of the given vertex, building the
        subgraph is made in O(deg(vertex)), and in order to maintain
        the integrity of both graphs, all the adjacency lists of the
        neighborhood of the given vertex is checked, so the overall
        complexity of the method is O(deg(vertex) * delta(N(vertex))),
        where N(vertex) is the neighborhood of 'vertex', and delta(S)
        is the maximum degree of the set of nodes S.
        
        Args:
          vertex (Node): the vertex whose neighborhood will induct the
            new subgraph.
        
        Complexity: O(|V| + |E|)
        
        Returns:
          GRAPH: a new GRAPH data structure, with only the vertices
            on the neighborhood of the vertex given and the edges
            between them inside of it.
        """
        subgraph = GRAPH()
        
        # Adds the neighborhood to the subgraph
        for neighbor in vertex.data:
            subgraph.vertices.append(self.vertices.remove(neighbor.nid))
            self.m -= 1
            subgraph.m += 1
            
        # We update the adjacency list of the original graph
        for sub_vertex in subgraph.vertices:
            bucket = len(sub_vertex)
        
            # Check all the neighbors imported from original graph
            for neighbor in sub_vertex.data:
            
                # Delete edges not included on the subgraph
                if neighbor.nid not in subgraph.vertices:
                    self.degrees.decrease(self.vertices[neighbor.nid])
                    self.n -= 1
                    
                    # Updates the adjacency list of the graph
                    self.vertices[neighbor.nid].data.remove(sub_vertex.nid)
                    subgraph.vertices[sub_vertex.nid].data.remove(
                      neighbor.nid)
                else:
                    if sub_vertex.nid < neighbor.nid:
                        self.n -= 1
                    
            # Updates the number of edges in the subgraph
            subgraph.n += len(sub_vertex)
                    
            # Finally, we delete the vertices from the original
            # graph's DEGREE
            self.degrees.buckets[bucket].data.remove(sub_vertex.nid)
            
            # Also, check if the max degree bucket has become empty
            if (bucket == self.degrees.max_degree 
                  and self.degrees.buckets[bucket].data.is_empty()):
                current_degree = self.degrees.buckets.first
                
                while (current_degree is not None 
                      and current_degree.data.is_empty()):
                    current_degree = current_degree.tail
                    
                if current_degree is not None:
                    self.degrees.max_degree = current_degree.nid
                else:
                    self.degrees.max_degree = 0
                    
            # Or if the min degree bucket has become empty
            if(bucket == self.degrees.min_degree
                  and self.degrees.buckets[bucket].data.is_empty()):
                current_degree = self.degrees.buckets.last
                
                while (current_degree is not None
                      and current_degree.data.is_empty()):
                    current_degree = current_degree.head
                    
                if current_degree is not None:
                    self.degrees.min_degree = current_degree.nid
                else:
                    self.degrees.min_degree = SENTINEL
        
        # Since every edge is counted twice (once for each adjacent
        # vertex), the number of edges needs to be halved.
        subgraph.n = int(subgraph.n / 2)
        
        return subgraph


class DEGREE(object):
    """Implements the DEGREE data structure as defined by Widgerson.
    
    DEGREE is used to maintain the degree of each vertex, so that it
    can be updated in constant time with each removal of an edge, and
    have a constant time access to a vertex of maximum degree.
    
    Let d1 >= d2 >= ... >= dp the degree values occurring in the graph.
    For each di, we keep a "bucket" Di. These buckets are doubly linked
    in the above order, and we have a pointer to the first bucket, D1. 
    In ecah bucket Di we keep all vertices of degree di, doubly linked 
    in some order. Every Di points to the first vertex in it, so we can
    tell when it gets empty. Each vertex in GRAPH will point to its 
    place in the appropriate bucket in DEGREE.
    
    Attributes:
      buckets (DoublyLinkedList): the linked list that contains the
        degrees occurring in the GRAPH.
      max_degree (int): the value for the maximum degree currently 
        occurring in the graph.
      min_degree (int): the value for the minimum degree currently
        occurring in the graph.
    """
    
    def __init__(self):
        """Creates a new DEGREE data structure.
        
        Complexity: O(1)
        """
        self.buckets = DoublyLinkedList()
        self.max_degree = 0
        self.min_degree = SENTINEL
        
    def __getitem__(self, deg):
        """Recovers the first vertex with the degree given.
        
        Since a pointer to the first element in each list is 
        always kept, getting the first element of a list takes
        O(1) time.
        
        If no vertex in the graph has the degree given, None
        is returned instead.
        
        Args:
          deg (int): the degree of a vertex.
          
        Complexity: O(1)
          
        Return:
          Node: the first vertex with the degree specified, or None if
            no vertex with the given degree exists.
        """
        if deg not in self.buckets:
            return None
        elif not self.buckets[deg].data.is_empty():
            return self.buckets[deg].data.first
        else:
            return None
            
    def __str__(self):
        """Get a string representation of the DEGREE.
        
        Since all vertices are required in the representation, this
        method takes O(|V|) to run.
        
        Complexity O(|V|)
        
        Returns:
          string: a representation of the DEGREE.
        """
        bucks = []
        
        for bucket in self.buckets:
            bucks.append("Bucket {0}:\n{1}".format(
                bucket.nid, str(bucket.data)))
            
        return "\n".join(bucks)
    
    def add(self, vertex):
        """Add a vertex to the right bucket in the data structure.
        
        If the bucket already exists, the vertex is just added at
        the end of the bucket, which takes O(1) time. If the bucket 
        does not exists, a new bucket is created and the vertex is
        added to it, which takes O(|V|) time (since all the buckets 
        need to be checked, and in the worst case there can be |V| 
        buckets if every vertex has a different degree). The pointer
        to the max bucket is also updated if needed, which takes O(1).
        Therefore, the overall complexity of the method is O(|V|).
        
        Args:
          vertex (Node): the node to be placed in the right bucket.
        
        Complexity: O(|V|)
        
        Returns:
          boolean: True if and only if the node given is placed in
            its right bucket. False otherwise.
        """
        deg = len(vertex)
        
        # Checks if the length is not the sentinel value
        if deg == SENTINEL:
            return False
        
        # If a bucket of the given size exists, only add the node to it
        if deg in self.buckets:
            # Create the copy of the vertex
            copy_vertex = Node(vertex.nid)
            
            # Links the node in the GRAPH to its copy on DEGREE
            vertex.bucket = copy_vertex
            copy_vertex.data = vertex
            
            # Appends the copy vertex to the bucket
            self.buckets[deg].data.append(copy_vertex)
            
            return True
        # If the bucket of given size does not exists, is created
        else:
            # Create the new bucket
            self.buckets.insert(deg)
            self.buckets[deg].data = DoublyLinkedList()
            
            # Create the copy of the vertex
            copy_vertex = Node(vertex.nid)
            
            # Links the node in the GRAPH to its copy on DEGREE
            vertex.bucket = copy_vertex
            copy_vertex.data = vertex
            
            # Appends the copy vertex to the bucket
            self.buckets[deg].data.append(copy_vertex)
            
            # Also checks if new bucket is bigger than max degree...
            if deg > self.max_degree:
                self.max_degree = deg
                
            # ...or smaller than min degree
            if deg < self.min_degree:
                self.min_degree = deg
                
            return True
            
    def decrease(self, vertex):
        """Decrease in 1 the degree of a vertex.
        
        This method is called whenever an edge is deleted from a
        GRAPH. The adjacency list of the given vertex is NOT modified
        in order to maintain the linear complexity of the method. This
        method only moves the vertex from its current bucket to the
        bucket inmediately after the current bucket (if said bucket
        does not exists, it is created in place). Since the operation
        only involves removing the vertex from one bucket to another,
        it takes O(1) time to complete.
        
        Args:
          vertex (Node): the node whose degree will be decreased by 1.
          
        Complexity: O(1)
        """
        deg = len(vertex)

        copy_vertex = self.buckets[deg].data.remove(vertex.bucket.nid)
        
        # Checks if the bucket len - 1 exists
        if (deg - 1) in self.buckets:
            # Adds the vertex to its new bucket
            self.buckets[deg - 1].data.append(copy_vertex)
        # If the bucket does not exists, it must be created
        else:
            # Creates the new bucket
            new_node = Node(deg - 1)
            
            # Inserts the bucket in place
            new_node.tail = self.buckets[deg].tail
            new_node.head = self.buckets[deg]
            
            # Checks if the new bucket is not the last
            if self.buckets[deg].tail is not None:
                self.buckets[deg].tail.head = new_node
            else:
                self.buckets.last = new_node
                
            self.buckets[deg].tail = new_node
            
            # Adds the new bucket to the dictionary of buckets
            self.buckets.elements[deg - 1] = new_node
            
            # Creates the new bucket's list
            new_node.data = DoublyLinkedList()
            
            # Adds the vertex to its new bucket
            new_node.data.append(copy_vertex)
            
# ------------------------------------------------------------------- #
#                            Utily methods                            #
# ------------------------------------------------------------------- #

def from_dimacs(filename):
    """Load a graph stored in the DIMACS format.
    
    In the DIMACS format, every line of the input begins with a letter
    that defines the content of that line. The legal lines are:
    
      * c : Comment. The rest of the line should be ignored.
      * p : Problem. Must be of form 'p edges m n' where m is the
            number of nodes (to be numbered 1...m) and n is the
            number of edges.
      * e : Edge. Must be of form 'e n1 n2 d' where n1 and n2 are
            the endpoints of the edge. The optional d value is used
            to enforce a requirement and n1 and n2 have colors that
            differ by at least d (if d is not provided, it is assumed
            d=1)
      * f : Fixed. Must be of form 'f n1 c1 c2 c3...' and states that
            node n1 must choose its colors from c1, c2, c3, ... (if
            not provided, it is assumed that the node can take any
            color).
      * n : Node. Must be of the form 'n n1 c1' used in multicoloring
            to state that c1 colors must be assigned to node n1. If
            not provided, is assumed that the node must be assigned
            only one color. These colors must all differ by at least 1,
            unless there is an edge of the form 'e n1 n1 d' in which
            all colors at n1 must differ by at least d.
            
    Since the DIMACS format only specifies edges, this method takes
    O(|E|) to complete.
    
    Args:
      filename (string): the full path to the text file containing the
        specification of the graph.
        
    Complexity: O(|E|).
        
    Raises:
      SyntaxError: if the DIMACS syntax is incorrect or does not
      correspond to a valid graph syntax.
    """
    g = GRAPH()
    
    with open(filename, "r") as f:
        for line in f:
            # Comments are ignored
            if line.startswith("c"):
                continue
            
            # There should be 1 and only 1 p line.
            if line.startswith("p"):
                specs = line.split(" ")
                m = int(specs[2])
                n = int(specs[3])
                
                for i in range(1, m + 1):
                    g.add_vertex(i)
                
                continue
            
            # Most lines of the graph are edges
            if line.startswith("e"):
                # Currently, the algorithm only support 
                ends = line.split(" ")
                ea = int(ends[1])
                eb = int(ends[2])
                
                g.add_edge(ea, eb)
                
                continue
                
    return g
    
def from_json(filename):
    """Load a graph stored in JSON format.
    
    The JSON format accepted by the parser was defined as part of the
    Java Graph Viewer Engine, and follows this syntax:
    
      {
        "vertices" : [
            {
                "vid" : << Vertex ID >>,
                "label" : "<< Vertex color class, or NULL >>",
                "neighbors" : [ << Array of neighbors' IDS >> ]
            } , ...
        ],
        
        "edges" : [
            {
                "endpoints" : [ << Vertex ID A >>, << Vertex ID B >> ],
                "directed" : << false | true >>
            } , ...
        ]  
      }
      
    Args:
      filename (String): the name of the file that contains the JSON
        specification of the GRAPH.
        
    Returns:
      GRAPH: the GRAPH stored in the file as a GRAPH data structure.
    """
    with open(filename, "r") as f:
        parsed_json = json.loads(f.read())
        
    g = GRAPH()
    
    # Recreate the vertices
    for i in range(len(parsed_json['vertices'])):
        vertex = parsed_json['vertices'][i]
        
        g.add_vertex(vertex['vid'])
        g.vertices[vertex['vid']].color = int(vertex['label'])
        
    # Recreate the edges
    for i in range(len(parsed_json['edges'])):
        edge = parsed_json['edges'][i]
        
        g.add_edge(int(edge['endpoints'][0]), int(edge['endpoints'][1]))
        
    # Builds the GRAPH's DEGREE
    g.build_DEGREE()
    
    return g
    
def to_dimacs(graph, filename):
    """Save a graph to a file in the DIMACS format.
    
    In the DIMACS format, every line of the input begins with a letter
    that defines the content of that line. The legal lines are:
    
      * c : Comment. The rest of the line should be ignored.
      * p : Problem. Must be of form 'p edges m n' where m is the
            number of nodes (to be numbered 1...m) and n is the
            number of edges.
      * e : Edge. Must be of form 'e n1 n2 d' where n1 and n2 are
            the endpoints of the edge. The optional d value is used
            to enforce a requirement and n1 and n2 have colors that
            differ by at least d (if d is not provided, it is assumed
            d=1)
      * f : Fixed. Must be of form 'f n1 c1 c2 c3...' and states that
            node n1 must choose its colors from c1, c2, c3, ... (if
            not provided, it is assumed that the node can take any
            color).
      * n : Node. Must be of the form 'n n1 c1' used in multicoloring
            to state that c1 colors must be assigned to node n1. If
            not provided, is assumed that the node must be assigned
            only one color. These colors must all differ by at least 1,
            unless there is an edge of the form 'e n1 n1 d' in which all
            colors at n1 must differ by at least d.
    
    Since the DIMACS format does not (initially) support "node
    labeling", the IDs of the nodes of the graph are 'renamed'
    to a sequentially increasing ID's. The renaming of IDs are
    included at the beggining of the resulting file as comments.
    
    Args:
      graph (GRAPH): the GRAPH data structure to be saved.
      filename (string): the name of the file in which the GRAPH will
        be saved.
    """
    # Create the lines of the file
    lines = list()
    renames = dict()
    aux = 1

    lines.append("c file {0}\n".format(filename))
    lines.append("c\n")
    lines.append("c This file was automatically created")
    lines.append(" with 'datastructures.py' script.\n")
    lines.append("c The following changes were made to the graph:\nc\n")
    
    # 'Rename' the IDs of node to preserve the DIMACS standard
    for vertex in graph.vertices:
        renames[vertex.nid] = aux
        lines.append("c Node {0} renamed to {1}\n".format(vertex.nid, aux))
        aux += 1
        
    # Append the 'problem' line
    lines.append("c\np edge {0} {1}\n".format(graph.m, graph.n))
    
    # Now append the edges
    for vertex in graph.vertices:
        for neighbor in vertex.data:
            # Prevent duplicated edges
            if vertex.nid < neighbor.nid:
                lines.append("e {0} {1}\n".format(
                  renames[vertex.nid], renames[neighbor.nid]))
                  
    # Now save the graph
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
            
    print("Graph successfully saved as {0}".format(filename))

def to_json(graph, filename):
    """Save a graph to a file in the JSON format.
    
    The JSON format accepted by the parser was defined as part of the
    Java Graph Viewer Engine, and follows this syntax:
    
      {
        "vertices" : [
            {
                "vid" : << Vertex ID >>,
                "label" : "<< Vertex color class, or NULL >>",
                "neighbors" : [ << Array of neighbors' IDS >> ]
            } , ...
        ],
        
        "edges" : [
            {
                "endpoints" : [ << Vertex ID A >>, << Vertex ID B >> ],
                "directed" : << false | true >>
            } , ...
        ]  
      }
      
    Args:
      graph (GRAPH): the GRAPH data structure to be saved.
      filename (String): the name of the file that contains the JSON
        specification of the GRAPH.
    """
    json_g = dict()
    
    json_vertices = list()
    json_edges = list()
    
    for vertex in graph.vertices:
        jsonv = dict()
        jsonv["vid"] = vertex.nid
        jsonv["label"] = str(vertex.color)
        jsonv["neighbors"] = list(vertex.data.elements.keys())
        
        json_vertices.append(jsonv)
        
        for neighbor in vertex.data:
            if vertex.nid < neighbor.nid:
                jsone = dict()
                jsone["endpoints"] = [vertex.nid, neighbor.nid]
                jsone["directed"] = False
                
                json_edges.append(jsone)
                
    json_g["vertices"] = json_vertices
    json_g["edges"] = json_edges
    
    with open(filename, "w") as f:
        f.write(json.dumps(json_g))
        
    print("Graph successfully saved as {0}".format(filename))
