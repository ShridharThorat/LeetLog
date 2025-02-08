class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        
def edges_to_dict(adjList= [[2,4],[1,3],[2,4],[1,3]]):
    """Takes a list of edges, where the index+1 is the node, and the list at the index are its edges"""
    
    graph_dict ={} # key - val, val = node
    
    for i,neighbours in enumerate(adjList):
        graph_dict[i+1] = Node(i+1)
        
        for n in neighbours:
            if n not in graph_dict[i+1]:
                graph_dict[n] = Node(n)
            graph_dict[i+1].neighbors.append(graph_dict[n])
    
    return graph_dict[1]

        
