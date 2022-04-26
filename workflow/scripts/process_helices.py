from utils import read_gr_file, add_element_to_adj
import sys

sys.setrecursionlimit(10000)

## TREE DECOMPOSITION MANIPULATION FUNCTIONS ##
def add_clique_case_subtree(subtree_root, 
                            clique_case_index,
                            abcd,
                            adj,
                            index2bag,
                            graph_adj):
    """
    Args:
        - subtree_root: the index of the bag that was
        seen to contain the four extremities of the 
        helix. we will attach to it a bag containing
        just the four extremities of the helix,
        where will be rooted a sub-tree decomposition
        containing the helix

        - clique_case_index: The index for the
        bag containing only the 4 extremities. I.e.
        the separator. This index is not just a number:
        it contains the name of the helix as well.

        - abcd: the separator, as a list.

        `- adj: the adjacency of the tree. will be modified
        to include the helix.

        - index2bag: dictrionary from indices to bag content

        - graph_adj: graph adjacency dictionnary: used to detect
        when in bulges (vertices have degree=2 in them)
    """
    
    # clique separator bag
    index2bag[clique_case_index] = abcd
    adj[clique_case_index] = [subtree_root]
    adj[subtree_root] = [clique_case_index]

    # bag succession, built from elimination order
    x = abcd[0] # will increase
    y = abcd[1] # will decrease

    elimination_ordering = []

    while x < abcd[0] or y > abcd[1]:
        # eliminating bulges:
        u = x+1
        while len(graph_adj[u])==2:
            elimination_ordering.append(u)
            u += 1

        v = y-1
        while len(graph_adj[v])==2:
            elimination_ordering.append(v)
            v -= 1 
            
        # eliminating x & y:
        elimination_ordering.append(x)
        elimination_ordering.append(y)

        x = u
        y = v

    # from elimination ordering to bags:
    cnt = 0
    while len(elimination_ordering) > 0:
        vertex = elimination_ordering.pop(0)

        bag = [vertex] + [v for v in elimination_ordering if v in adj[u]]
        index2bag[clique_case_index+'-'+str(cnt)] = bag
        cnt += 1

    for new_bag_index in range(0,cnt+1,1):
        if new_bag_index==0:
            adj[clique_case_index+'-'+str(cnt)] = [clique_case_index+'-1']
        elif new_bag_index==cnt:
            adj[clique_case_index+'-'+str(cnt)] = [clique_case_index+'-'+str(cnt-1),clique_case_index]
        else:
            adj[clique_case_index+'-'+str(cnt)] = [clique_case_index+'-'+str(cnt-1),clique_case_index+'-'+str(cnt+1)]
        
    return adj, index2bag
    
def in_helix(u, abcd):
    if (u >= abcd[0]) or (u<=abcd[2]):
        return True
    if (u >= abcd[3]) or (u<=abcd[1]):
        return True
    return False

def counterpart(x):
    if x < 2:
        return 1-x
    else:
        return 1-(x-2)+2

def opposites(x):
    if x < 2:
        return 2,3
    else:
        return 0,1
    

def diag_canonicize(u, v, x, helixname, abcd, adj, index2bag):
    """
    At the end of the processing, the bag indexed by
    u will have been modified to contain (helix-wise) 
    x and its counter part. v on the other
    end will contain both extremities of the other end.

    Args:
        - u: index of one of the bags adjacent to the tree
        decomposition edge that separates abcd[x] from the
        opposite end of the helix. abcd[x] is on the u-side
        of the edge.

        - v: index of the other bag, forming with u 
        a tree decomposition edge that separates x from 
        the other extremity of the helix. both
        vertices on the other extremity of the helix
        are on the v-side

        - x: either 0,1,2 or 3: abcd[x] is separated
        from both vertices of the opposite end of the
        helix by the tree decomposition edge (u,v).
        it is on the u-side while the opposite end
        is on the v-side.

        - helixname: to label bags

        - abcd: the extremities of the helix

        - adj: tree decomposition adjacency

        - index2bag: bag content dictionary

    Returns:
        - adj, index2bag: modified versions.
    """
    
    # the intersection of u and v 
    sep = set(index2bag[u]).intersection(set(index2bag[v]))

    # removing from it vertices of the helix (to get the
    # part that will be constant in the subtree decomposition
    # corresponding to the helix.)

    sep = [u for u in sep if not in_helix(u, abcd)]

    y = counterpart(x)
    s, t = opposites(x)

    # replacing, on u-side, occurences of things other than x,y
    def find_path(x,v,u,l):
        if x in index2bag[u]:
            return l
        else:
            for w in adj[u]:
                if w!=v:
                    return find_path(x,u,w,l+[u])

   
    path_x = find_path(x,v,u,[])
    path_y = find_path(y,v,u,[])

    for b in path_x:
        index2bag[b] = [vertex for vertex in index2bag[b] if not inhelix(vertex) or vertex == y]
    for b in path_y:
        index2bag[b] = [vertex for vertex in index2bag[b] if not inhelix(vertex) or vertex == x]

    # replacing, on the v-side, occurences of things other than s,t
    path_s = find_path(s,u,v,[])
    path_t = find_path(t,u,v,[])

    for b in path_s:
        index2bag[b] = [vertex for vertex in index2bag[b] if not inhelix(vertex) or vertex == t]
    for b in path_t:
        index2bag[b] = [vertex for vertex in index2bag[b] if not inhelix(vertex) or vertex == s]


    # new bags
    cnt = 0

    first_bag = sep + [x,y]
    index2bag[helixname+'-'+str(cnt)] = first_bag
    cnt+=1

    last_bag = sep + [s,t]
    
    u = x
    v = y

    dir_u = 1 if x<s else -1
    dir_v = 1 if y<v else -1

    switch = True

    cur_bag = first_bag
    to_forget_u = None
    to_forget_v = None

    # to avoid code duplication:
    def move_along(u, dir_u, to_forget_u, cur_bag, cnt):
        # move
        u += dir_u
        # new bag
        cur_bag = [vertex for vertex in cur_bag if vertex != to_forget_u]
        cur_bag.append(u)
        index2bag[helixname+'-'+str(cnt)] = cur_bag
        cnt+=1
        # next to forget
        to_forget_u = u-dir_u

        return u, dir_u, to_forget_u, cur_bag, cnt

    while u!=s or v!=t:
        if switch and u!=s:
            # treating potential bulge
            while len(graph_adj[u+dir_u])==2:
                u, dir_u, to_forget_u, cur_bag, cnt = move_along(u, dir_u, to_forget_u, cur_bag, cnt)

            # next paired vertex
            u, dir_u, to_forget_u, cur_bag, cnt = move_along(u, dir_u, to_forget_u, cur_bag, cnt)

        if not switch and v!=t:
            # treating potential bulge
            while len(graph_adj[v+dir_v])==2:
                v, dir_v, to_forget_v, cvr_bag, cnt = move_along(v, dir_v, to_forget_v, cvr_bag, cnt)
            
            # next paired vertex
            v, dir_v, to_forget_v, cvr_bag, cnt = move_along(v, dir_v, to_forget_v, cvr_bag, cnt)

        switch = not switch

    # reconnecting everything
    index2bag[helixname+'-'+str(cnt)] = last_bag
    
    for index in range(0, cnt, 1):
        adj = add_element_to_adj(adj,helixname+'-'+str(cnt), helixname+'-'+str(cnt+1))
        adj = add_element_to_adj(adj,helixname+'-'+str(cnt+1), helixname+'-'+str(cnt))

    return adj, index2bag


# extracting graph adj from gr file
graph_adj = read_gr_file(open(snakemake.input.graph).readlines())

# extracting bags and tree from td file
index2bag = {}
adj = {}

started_bs = False

for line in open(snakemake.input.tdname).readlines():
    if line[0]=='b':
        started_bs = True
        index2bag[line.split(' ')[1]] = [vertex.rstrip('\n') for vertex in line.split(' ')[2:]]

    else:
        if started_bs:
            i = line.split(' ')[0]
            j = line.split(' ')[1].rstrip('\n')
            try:
                adj[i].append(j)
            except KeyError:
                adj[i] = [j]
            try:
                adj[j].append(i)
            except KeyError:
                adj[j] = [i]


# connecting tree dec
root = index2bag['1']


# set of extremities
extremities = []
for hline in open(snakemake.input.helix).readlines():
    abcd = hline.split('(')[1].split(')')[0].split(',')
    extremities += abcd
extremities = set(extremities)

def fill_ext_below(index2bag, adj, extremities, root):

    ext_below = {} # "below", same 

    def fill_below(u,v):
        if (u,v) in ext_below.keys():
            return ext_below[(u,v)]

        ext_below[(u,v)] = set(index2bag[v]).intersection(extremities)

        for w in adj[v]:
            if w!=u:
                ext_below[(u,v)] = ext_below[(u,v)].union(fill_below(v,w))

        return ext_below[(u,v)]

    fill_below('-1', root)

    return ext_below

ext_below = fill_ext_below(index2bag, adj, extremities, '1')

def fill_ext_above(index2bag, adj, extremities, root, ext_below):

    ext_above = {}

    def fill_above(t,u,v,acc):

        ext_above[(u,v)] = set(index2bag[u]).intersection(extremities)
        ext_above[(u,v)].union(acc)

        for w in adj[u]:
            if w!=v and w!=t:
                ext_above[(u,v)].union(ext_below[(u,w)])

        
        for w in adj[v]:
            if w!=u:
                fill_above(u,v,w,ext_above[(u,v)])
    
    for u in adj[root]:
        fill_above('-1',root, u, set([]))

    return ext_above

ext_above = fill_ext_above(index2bag, adj, extremities, '1', ext_below)

# helix processing
for hline in open(snakemake.input.helix).readlines():
    abcd = hline.split('(')[1].split(')')[0].split(',')
    helixname = hline.split(' ')[0]
    # detecting clique case
    clique_case = False
    subtree_root = -1
    
    for index, bag in index2bag.items():
        if set(abcd).issubset(set(bag)):
            clique_case = True
            subtree_root = index
            break
                
    if clique_case:
        # building subtree
        # containing abcd
        adj, index2bag = add_clique_case_subtree(subtree_root, 
                                                 hline.split(' ')[0],
                                                 abcd,
                                                 adj,
                                                 index2bag,
                                                 graph_adj)

    # detecting diag case
    diag_case = False
    sep = (-1,-1)

    # iterating over all edges of the tree decomposition
    # in a dfs way
    queue = [('1', ngbh) for ngbh in adj['1']]
        
    while len(queue) > 0:
        u,v = queue.pop()

        inter = set(index2bag[u]).intersection(set(index2bag[v]))

        above = ext_above[(u,v)]
        below = ext_below[(u,v)]

        if abcd[0] in above and abcd[2] in below and abcd[3] in below: 
        # if 0 on u-side
        # and opposite extremities on v side
            adj, index2bag = diag_canonicize(u, v, 0, helixname, abcd, adj, index2bag)
            break
        if abcd[2] in above and abcd[0] in below and abcd[1] in below: 
            adj, index2bag = diag_canonicize(u, v, 2, helixname, abcd, adj, index2bag)
            break
        if abcd[1] in above and abcd[2] in below and abcd[3] in below: 
            adj, index2bag = diag_canonicize(u, v, 1, helixname, abcd, adj, index2bag)
            break
        if abcd[3] in above and abcd[0] in below and abcd[1] in below: 
            adj, index2bag = diag_canonicize(u, v, 3, helixname, abcd, adj, index2bag)
            break
        
        if abcd[0] in below and abcd[2] in above and abcd[3] in above: 
        # if 0 on v-side
        # and o[pposite extremities on u side
            adj, index2bag = diag_canonicize(v, u, 0, helixname, abcd, adj, index2bag)
            break
        if abcd[2] in below and abcd[0] in above and abcd[1] in above: 
            adj, index2bag = diag_canonicize(v, u, 2, helixname, abcd, adj, index2bag)
            break
        if abcd[1] in below and abcd[2] in above and abcd[3] in above: 
            adj, index2bag = diag_canonicize(v, u, 1, helixname, abcd, adj, index2bag)
            break
        if abcd[3] in below and abcd[0] in above and abcd[1] in above: 
            adj, index2bag = diag_canonicize(v, u, 3, helixname, abcd, adj, index2bag)
            break

        for w in adj[v]:
            if w!=u:
                queue.append((v,w))

# writing output (finally)
f = open(snakemake.output[0],'w')

# header line
print('s td '+str(len(index2bag.keys()))+' ', end="", file=f)

# largest bag size
width = max([len(val) for _, val in index2bag.items()])
print(str(width)+' NVERTICES', file=f)


for key, val in index2bag.items():
    print('b',key,end=" ",file=f)
    for vertex in val:
        print(vertex, end=" ",file=f)
    print("", file=f)

queue = [('1',ngbh) for ngbh in adj['1']]

while len(queue) > 0:
    u,v = queue.pop()
    print(u,v,file=f)
    for w in adj[v]:
        if w!=u:
            queue.append((v,w))
