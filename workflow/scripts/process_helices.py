from utils import read_gr_file, add_element_to_adj
import sys

sys.setrecursionlimit(10000)

## TREE DECOMPOSITION MANIPULATION FUNCTIONS ##
def add_clique_case_subtree(subtree_root, 
                            helixname,
                            i,ip,jp,j,
                            adj,
                            index2bag):
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
    
    cur_i = i
    cur_j = j
    cnt = 0
    prev_bag = subtree_root
    cur_bag = helixname+'-'+str(cnt)
    iturn = True
    const = [str(ip),str(jp)]

    while cur_i < ip or cur_j > jp:
        if iturn:
            # build
            bag_content = [str(cur_i),str(cur_j),str(cur_i+1)] + const
            index2bag[cur_bag] = bag_content
            adj[prev_bag].append(cur_bag)
            adj[cur_bag] = [prev_bag]

            # update
            cur_i += 1
            prev_bag = cur_bag
            cnt += 1
            cur_bag = helixname+'-'+str(cnt)
            iturn = False
        else:
            #jturn, build
            bag_content = [str(cur_i),str(cur_j),str(cur_j-1)] + const
            index2bag[cur_bag] = bag_content
            adj[prev_bag].append(cur_bag)
            adj[cur_bag] = [prev_bag]

            # update
            cur_j -= 1
            prev_bag = cur_bag
            cnt += 1
            cur_bag = helixname+'-'+str(cnt)
            iturn = True

    return adj, index2bag
    

def replace(u,v,lo,hi,val,to_keep_safe,adj,index2bag):
    """
    (u,v) must be an edge of the tree
    decomposition.
    starting from u and in the direction
    of v, all indices/vertices
    contained in the interval [lo,hi]
    are replaced with val
    """
    print("from",u,"towards",v,"replacing from ", lo, "to", hi, "with", val)

    queue = [(u,v)]

    while len(queue) > 0:
        u,v = queue.pop()
        assert(u in adj[v])
        new_content = []
        for vertex in index2bag[v]:
            if vertex[0]=='H':
                new_content.append(vertex)
                continue
            if int(vertex) >= lo and int(vertex) <= hi and vertex not in to_keep_safe:
                new_content.append(str(val))
                #print("replacing",vertex,"with",val,"in bag",v)
            else:
                new_content.append(vertex)

        index2bag[v] = new_content

        for w in adj[v]:
            if w!=u:
                queue.append((v,w))

    return index2bag

def shift_separator(u,v,i,j,ip,jp,inter,adj,index2bag,vert_above,vert_below):
    """
    we do not want to canonicize a diag case with an extremity 
    in the separator
    """
    above = vert_above[(u,v)]
    below = vert_below[(u,v)]

    if str(i) in inter:
        extremity = i
        replacement = i-1
    if str(j) in inter:
        extremity = j
        replacement = j+1
    if str(ip) in inter:
        extremity = ip
        replacement = ip+1
    if str(jp) in inter:
        extremity = jp
        replacement = ip-1

    new_bag_content = list(inter)+[str(replacement)]
    new_bag_label = 'shift-'+u
    print("shifting from",extremity,"to",replacement, "td edge", u,v)
    if str(replacement) in above:
        print("above case")
        
        # modifying bag dictionary
        index2bag = replace(v,u,extremity,extremity,replacement,[],adj,index2bag)
        index2bag[new_bag_label] = new_bag_content

        # modifying edges
        adj[u] = [bag for bag in adj[u] if bag!=v] + [new_bag_label]
        adj[v] = [bag for bag in adj[v] if bag!=u] + [new_bag_label]
        adj[new_bag_label] = [u,v]
    
        # modifying dict for vertices above and below:
        vert_above[(u, new_bag_label)] = set([vertex for vertex in vert_above[(u,v)] if vertex!=extremity])
        vert_below[(u, new_bag_label)] = vert_below[(u,v)].union(set([replacement]))
        vert_above[(new_bag_label,v)] = vert_above[(u,v)]
        vert_below[(new_bag_label,v)] = vert_below[(u,v)]

        vert_below.pop((u,v))
        vert_above.pop((u,v))

        # which edge holds the separator now ?
        v = new_bag_label
        return adj, index2bag, vert_above, vert_below, u, v

    if str(replacement) in below:
        print("below case")
        index2bag = replace(u,v,extremity,extremity,replacement,[],adj,index2bag)
        index2bag[new_bag_label] = new_bag_content

        # modifying edges
        adj[u] = [bag for bag in adj[u] if bag!=v] + [new_bag_label]
        adj[v] = [bag for bag in adj[v] if bag!=u] + [new_bag_label]
        adj[new_bag_label] = [u,v]
        
        # modifying dict for vertices above and below:
        vert_above[(u, new_bag_label)] = vert_above[(u,v)]
        vert_below[(u, new_bag_label)] = vert_below[(u,v)]
        vert_above[(new_bag_label,v)] = vert_above[(u,v)].union(set([replacement]))
        vert_below[(new_bag_label,v)] = set([vertex for vertex in vert_below[(u,v)] if vertex!=replacement])

        vert_below.pop((u,v))
        vert_above.pop((u,v))
    
        # which edge holds the separator now ?
        u = new_bag_label
        return adj, index2bag, vert_above, vert_below, u, v

def diag_canonicize(u,v,i,j,ip,jp,helixname, adj, index2bag):
    """
    in direction of u, replaces all helix occurences
    with i,j. same in direction of v with ip,jp
    puts intermediary bags in between for helix.
    """
    inter = set(index2bag[u]).intersection(set(index2bag[v]))

    print("diag cano call", i,j,ip,jp)
    print("diag cano call", u,v)
    print("inter ", inter)

    to_keep_safe = inter.intersection(set([str(c) for c in [i,j,ip,jp]]))

    ## replacements 
    index2bag = replace(v,u,i,ip,i,to_keep_safe,adj,index2bag)
    index2bag = replace(v,u,jp,j,j,to_keep_safe,adj,index2bag)
    index2bag = replace(u,v,i,ip,ip,to_keep_safe,adj,index2bag)
    index2bag = replace(u,v,jp,j,jp,to_keep_safe,adj,index2bag)

    ## insertions of new bags

    # disconnecting
    adj[u] = [b for b in adj[u] if b != v]
    adj[v] = [b for b in adj[v] if b != u]

    # constant part, inter without helix, except extremities
    const = [vertex for vertex in inter if int(vertex) <= i or int(vertex) >= j or (int(vertex) >= ip and int(vertex) <= jp)]

    print("diag-canonicizing ", helixname, "const part:", const)

    # let it be clear:
    index2bag[u] = list(const) + [str(i),str(j)]
    index2bag[v] = list(const) + [str(ip),str(jp)]

    # new intermediary bags
    cur_i = i
    cur_j = j
    cur_bag = u
    cnt = 0

    i_turn = True

    while cur_i < ip or cur_j > jp:
        prev_bag = cur_bag
        cur_bag = helixname +'-'+ str(cnt)
        if i_turn:
            index2bag[cur_bag] = list(const) + [str(cur_i), str(cur_j), str(cur_i+1)]
            adj[prev_bag].append(cur_bag)
            adj[cur_bag] = [prev_bag]
            cur_i += 1
            i_turn = False

        else:
        # turn of j to move
            index2bag[cur_bag] = list(const) + [str(c) for c in [cur_i, cur_j, cur_j-1]]
            adj[prev_bag].append(cur_bag)
            adj[cur_bag] = [prev_bag]
            cur_j -= 1
            i_turn = True
        cnt += 1

    # connecting to last bag (v)
    adj[cur_bag].append(v)
    adj[v].append(cur_bag)

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

def fill_vertices_below(index2bag, adj, extremities, root):

    vert_below = {} # "below", same 

    def fill_below(u,v):
        if (u,v) in vert_below.keys():
            return vert_below[(u,v)]

        vert_below[(u,v)] = set(index2bag[v])#.intersection(extremities)

        for w in adj[v]:
            if w!=u:
                vert_below[(u,v)] = vert_below[(u,v)].union(fill_below(v,w))

        return vert_below[(u,v)]

    fill_below('-1', root)

    return vert_below

vert_below = fill_vertices_below(index2bag, adj, extremities, '1')

def fill_vertices_above(index2bag, adj, extremities, root, ext_below):

    vert_above = {}

    def fill_above(t,u,v,acc):

        vert_above[(u,v)] = set(index2bag[u])#.intersection(extremities)
        vert_above[(u,v)] = vert_above[(u,v)].union(acc)

        for w in adj[u]:
            if w!=v and w!=t:
                vert_above[(u,v)] = vert_above[(u,v)].union(vert_below[(u,w)])
        
        for w in adj[v]:
            if w!=u:
                fill_above(u,v,w,vert_above[(u,v)])


    for u in adj[root]:
        fill_above('-1',root, u, set([]))

    return vert_above

vert_above = fill_vertices_above(index2bag, adj, extremities, '1', vert_below)

width = max([len(val) for key, val in index2bag.items()])-1

# helix processing
for hline in open(snakemake.input.helix).readlines():

    processed = False

    extremities = hline.split('(')[1].split(')')[0].split(',')
    helixname = hline.split(' ')[0]
    print("helix ", hline)

    i = int(extremities[0]) 
    j = int(extremities[1])
    ip = int(extremities[2])
    jp = int(extremities[3])

    print("bag 1", index2bag['1'])

    if width <= 3:
    # only diag case

        for k in range(1,ip-i):
            if processed:
                break
            for m in range(k+2,ip+1-i,1):
                if processed:
                    break
                # looking for a separator separating (i+k,j-k) and (i+m,j-m)

                # iterating over all edges of the tree decomposition
                # in a dfs way
                queue = [('1', ngbh) for ngbh in adj['1']]
                print(i+k,j-k,"sep",i+m, j-m," ?")
                    
                while len(queue) > 0:
                    u,v = queue.pop()
        
                    print("td edge u,v", u,v)
                    if u[0]=='H' or v[0]=='H':
                        for w in adj[v]:
                            if w!=u:
                                queue.append((v,w))
                        continue 

                    above = vert_above[(u,v)]
                    below = vert_below[(u,v)]

                    if str(i+k) in above-below and str(j-k) in above-below and str(i+m) in below-above and str(j-m) in below-above:
                        print("-->yes does sep !")
                        inter = set(index2bag[u]).intersection(set(index2bag[v]))
                        
                        # detecting specific extremity-in-separator case.
                        if any([str(vertex) in inter for vertex in [i,j,ip,jp]]):
                            print("will have to shift vertex")
                            adj, index2bag, vert_above, vert_below, u, v = shift_separator(u,v,i,j,ip,jp,inter,adj,index2bag,vert_above,vert_below)
                        
                        adj, index2bag = diag_canonicize(u,v,i,j,ip,jp,helixname,adj,index2bag)
                        processed = True
                        break
                    if str(i+k) in below-above and str(j-k) in below-above and str(i+m) in above-below and str(j-m) in above-below:
                        print("-->yes does sep !")

                        inter = set(index2bag[u]).intersection(set(index2bag[v]))
                        # detecting specific extremity-in-separator case.
                        if any([str(vertex) in inter for vertex in [i,j,ip,jp]]):
                            print("will have to shift vertex")
                            adj, index2bag, vert_above, vert_below, u, v = shift_separator(u,v,i,j,ip,jp,inter,adj,index2bag,vert_above,vert_below)

                        adj, index2bag = diag_canonicize(v,u,i,j,ip,jp,helixname,adj,index2bag)
                        processed = True
                        break

                    for w in adj[v]:
                        if w!=u:
                            queue.append((v,w))
            

        print("bag 1 out", index2bag['1'])
        # no need to check other cases. will do same for them, and check completeness at the end
        if processed:
            continue

    else:
    # else width >=4

        # detecting clique case = detecting hop edge
        found_hop = False
        for k in range(ip-i+1):
            if found_hop:
                break
            for m in range(ip-i+1):
                if found_hop:
                    break
                if abs(m-k) > 1:
                    # go over bags to see if one represents edge (i+k, j-m):
                    queue = [('-1','1')]

                    print("looking for edge ", i+k,j-m)

                    found_hop = False
                    while len(queue) > 0:
                        prev, u = queue.pop()
                        if str(i+k) in index2bag[u] and str(j-m) in index2bag[u]:
                            found_hop = True
                            # point to build G_clique minor
                            if k < m:
                                mid_point = k+1
                                ksupm = False
                            else:
                                mid_point = m+1
                                ksupm = True
                            break
                        for v in adj[u]:
                            if v!=prev:
                                queue.append((u,v))

        
        # then clique case
        if found_hop:
            print("found clique case")
            if ksupm:
                # to make substitution in whole tree: pick an edge and 
                # go in both directions from it
                v = adj['1'][0]

                # one direction
                index2bag = replace('1',v,i,i+mid_point,i,[],adj,index2bag)
                index2bag = replace('1',v,i+mid_point+1,ip,ip,[],adj,index2bag)
                index2bag = replace('1',v,jp,j-mid_point,jp,[],adj,index2bag)
                index2bag = replace('1',v,j-mid_point+1,j,j,[],adj,index2bag)
                # the other
                index2bag = replace(v,'1',i,i+mid_point,i,[],adj,index2bag)
                index2bag = replace(v,'1',i+mid_point+1,ip,ip,[],adj,index2bag)
                index2bag = replace(v,'1',jp,j-mid_point,jp,[],adj,index2bag)
                index2bag = replace(v,'1',j-mid_point+1,j,j,[],adj,index2bag)
            else: 
                v = adj['1'][0]
                index2bag = replace('1',v,i,i+mid_point-1,i,[],adj,index2bag)
                index2bag = replace('1',v,i+mid_point,ip,ip,[],adj,index2bag)
                index2bag = replace('1',v,jp,j-mid_point-1,jp,[],adj,index2bag)
                index2bag = replace('1',v,j-mid_point,j,j,[],adj,index2bag)
                index2bag = replace(v,'1',i,i+mid_point-1,i,[],adj,index2bag)
                index2bag = replace(v,'1',i+mid_point,ip,ip,[],adj,index2bag)
                index2bag = replace(v,'1',jp,j-mid_point-1,jp,[],adj,index2bag)
                index2bag = replace(v,'1',j-mid_point,j,j,[],adj,index2bag)

            # find bag with i,ip,jp,j
            queue = [('-1','1')]

            while len(queue) > 0:
                prev, u = queue.pop()

                if set([str(vert) for vert in [i,ip,jp,j]]).issubset(set(index2bag[u])):
                    adj, index2bag = add_clique_case_subtree(u, 
                                                             helixname,
                                                             i,ip,jp,j,
                                                             adj,
                                                             index2bag)
                    processed = True
                    break

                for v in adj[u]:
                    if v!=prev:
                        queue.append((u,v))
            
        else:
            print("did not find clique case, resorting to diag case.")
        # diag case. have to find ij/ipjp separator
            queue = [('1', ngbh) for ngbh in adj['1']]
                
            while len(queue) > 0:
                u,v = queue.pop()

                if u[0]=='H' or v[0]=='H':
                    for w in adj[v]:
                        if w!=u:
                            queue.append((v,w))
                    continue 

                above = vert_above[(u,v)]
                below = vert_below[(u,v)]

                if str(i) in above-below and str(j) in above-below and str(ip) in below-above and str(jp) in below-above:
                    adj, index2bag = diag_canonicize(u,v,i,j,ip,jp,helixname,adj,index2bag)
                    processed = True
                    break
                if str(i) in below-above and str(j) in below-above and str(ip) in above-below and str(jp) in above-below:
                    adj, index2bag = diag_canonicize(v,u,i,j,ip,jp,helixname,adj,index2bag)
                    processed = True
                    break

                for w in adj[v]:
                    if u!=w:
                        queue.append((v,w))

    # assert that helix has been processed, i.e. assert completeness of disjunction
    try:
        assert(processed) 
    except AssertionError:
        raise AssertionError

# writing output (finally)
f = open(snakemake.output[0],'w')

# header line
print('s td '+str(len(index2bag.keys()))+' ', end="", file=f)

# largest bag size
width = max([len(val) for _, val in index2bag.items()])
print(str(width)+' NVERTICES', file=f)

# removing adjacent redundancies

def substitute(vertex, v, u):
    if vertex==v:
        return u
    return vertex

smth_contracted = True

while smth_contracted:
    print('------------')
    smth_contracted = False
    queue = [('1',ngbh) for ngbh in adj['1']]

    while len(queue) > 0:
        u, v = queue.pop()
        if set(index2bag[u])==set(index2bag[v]) or set(index2bag[v]).issubset(set(index2bag[u])) or set(index2bag[u]).issubset(index2bag[v]):
            if (u[0]!='H') and (v[0]=='H'):
            # no hybrid contractions for clarity
                for w in adj[v]:
                    if w!=u:
                        queue.append((v,w))
                continue

            print("must contract !",v,"into",u,"(",index2bag[u],"<-",index2bag[v],")")
            smth_contracted = True
            adj[u] += adj[v]
            adj[u].remove(u)
            adj[u].remove(v)
            if set(index2bag[u]).issubset(set(index2bag[v])):
                index2bag[u] = index2bag[v]
            index2bag.pop(v)
            for w in adj[v]:
                adj[w] = [substitute(vertex, v,u) for vertex in adj[w]]
                if w!=u:
                    queue.append((u,w))
            adj.pop(v)
            continue

        for w in adj[v]:
            if w!=u:
                queue.append((v,w))



for key, val in index2bag.items():
    print('b',key,end=" ",file=f)
    for vertex in sorted(list(set(val))):
        print(vertex, end=" ",file=f)
    print("", file=f)

queue = [('1',ngbh) for ngbh in adj['1']]

while len(queue) > 0:
    u,v = queue.pop()
    print(u,v,file=f)
    for w in adj[v]:
        if w!=u:
            queue.append((v,w))


# Check correctness of TD
lines = open(snakemake.input.graph).readlines()[1:]
vertices = set([])
edges = set([])

for line in lines:
    u = line.split(' ')[0]
    v = line.split(' ')[1].rstrip('\n')
    vertices.add(u)
    vertices.add(v)
    edges.add((u,v))

correct = True

# auxiliary recursive functions
def represented(prev, u, s, index2bag, adj):
    if s.issubset(set(index2bag[u])):
        return True
    ans = False
    for v in adj[u]:
        if v!=prev:
            ans = ans or represented(u,v,s,index2bag,adj)
    return ans
            
def connected(prev, u, vertex, seen_above, currently_active, index2bag, adj):
    if vertex in index2bag[u]:
        if seen_above:
            if not currently_active:
                return False
        else:
            seen_above = True
            currently_active = True
    else:
        currently_active = False

    ans = True

    for v in adj[u]:
        if v!=prev:
            ans = ans and connected(u,v,vertex, seen_above, currently_active, index2bag, adj)

    return ans

# overall boolean
correct = True

print(adj.keys())
print(index2bag.keys())

for u in vertices:
    # represented
    try:
        assert(represented('-1','1', set([u]), index2bag, adj))
    except AssertionError:
        print(u, " not represened")
        raise AssertionError
    # in a connected way
    try:
        assert(connected('-1','1',u, False, False, index2bag, adj))
    except AssertionError:
        print("subtree", u, " not connected")
        raise AssertionError


for u,v in edges:
    try:
        assert(represented('-1','1', set([u,v]), index2bag, adj))
    except AssertionError:
        print(u,v," is not represented")
        raise AssertionError
