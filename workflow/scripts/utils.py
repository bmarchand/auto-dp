def add_element_to_adj(adj, vertex, new_neighbor):
    """
    simple try catch, just annoying to write all the time
    """
    try:
        adj[vertex].append(new_neighbor)
    except KeyError:
        adj[vertex] = [new_neighbor]

    return adj

def read_gr_file(lines):
    """
    Reads lines of a .gr file and 
    returns an adjacency graph
    """
    graph_adj = {}
    for line in lines[1:]:
        u = line.split(' ')[0]
        v = line.split(' ')[1].rstrip('\n')

        try:
            graph_adj[u].append(v)
        except KeyError:
            graph_adj[u] = [v]

        try:
            graph_adj[v].append(u)
        except KeyError:
            graph_adj[v] = [u]

    return graph_adj
