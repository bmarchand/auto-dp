def all_arcs(i,conf,n):
    if i==n:
        return [conf[:]]
    else:
        if conf[i]==-1:
            res = []
            for j in range(i+1,len(conf)):
                if conf[j]==-1:
                    (conf[i],conf[j]) = (j,i)
                    res += all_arcs(i+1,conf,n)
                    (conf[i],conf[j]) = (-1,-1)
        else:
            return all_arcs(i+1,conf,n)
        return res

def build_graph(perm):
    n=len(perm)
    arcs =[]
    adj = {}
    for i in range(n):
        if perm[i]>i:
            j = perm[i]
            adj[(i,j)] = []
            adj[(i,j)] = []
            for k in range(i+1,j):
                if perm[k]>j:
                    arcs.append(((i,j),(k,perm[k])))
                    break
    for bp1,bp2 in arcs:
        if bp1 not in adj:
            adj[bp1] = []
        adj[bp1].append(bp2)    
        if bp2 not in adj:
            adj[bp2] = []
        adj[bp2].append(bp1)    
    return adj

def flood(v,adj, found):
    if v not in found:
        found[v] = True        
        for w in adj[v]:
            flood(w,adj, found)
            
def generate_all_fat_graphs(k=3):
    conf = [-1 for i in range(2*k)]
    res = []
    for perm in all_arcs(0,conf,2*k):
        #print(perm)
        adj = build_graph(perm)
        nodes = list(adj.keys())
        #print(nodes)
        found = {}
        flood(nodes[0],adj, found)
        num_reached = len(found)
        connected = (num_reached == len(nodes))
        nested = False
        for i in range(len(perm)):
            if perm[i]>i:
                if perm[i+1]==perm[i]-1:
                    nested = True
                    break
        if connected and not nested:
            res.append(perm)
    return res

PARENTHESIS_SYSTEMS = ['()','[]','{}','<>','Aa','Bb','Cc','Dd','Ee','Ff','Gg','Hh','Ii']
k = 6
for perm in generate_all_fat_graphs(k):
    nbp = 0
    s = ['.' for i in range(2*k)]
    for i in range(len(perm)):
        if perm[i]>i:
            op,cp = PARENTHESIS_SYSTEMS[nbp]
            nbp += 1
            s[i] = op
            s[perm[i]] = cp
    print("".join(s))
