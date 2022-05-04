symbols = ["<>","()","[]","{}","Aa","Bb","Cc","Dd"]

stacks = {}

for s in symbols:
    stacks[s] = []

adj = {}

dbn = open(snakemake.input[0]).readlines()[0]

for k, c in enumerate(dbn):
    for s in symbols:
        if c==s[0]:
            stacks[s].append(k+1)
        if c==s[1]:
            l = stacks[s].pop()
            adj[k+1] = l
            adj[l] = k+1

#def complete_helix(u, v, adj):
#
#    # going to next bp
#    w = u+1
#    while w not in adj.keys():
#        w += 1
#
#    x = v-1
#    while x not in adj.keys():
#        x -= 1
#
#    if w >= x:
#        return u,v
#
#    if adj[x]!=w:
#        return u,v
#    else:
#        return complete_helix(w, x, adj)
#
#def find_helices(dbn, adj, i, j):
#
#    # swiping right for basal indices
#    index = i
#    basal_indices = []
#
#    while index < j:
#        try:
#            if index < adj[index]:
#                basal_indices.append((index, adj[index]))
#                index = adj[index]
#            else:
#                index += 1
#        except KeyError:
#            index += 1
#
#    # completing helices
#    helices = []
#
#    for u, v in basal_indices:
#        w, x = complete_helix(u, v, adj)
#        helices.append((u,v,w,x))
#        helices += find_helices(dbn,adj, w+1, x-1)
#
#    return helices

def find_helices(dbn, adj):

    # basal indices (largest overarching arc)
    basal_indices = []

    for i in range(1, len(dbn)+1,1):
        for j in range(i+1, len(dbn)+1,1):
            if j==adj[i]:
                try:
                    if j+1==adj[i-1]:
                        continue
                    else:
                        basal_indices.append((i,j))
                except KeyError:
                    basal_indices.append((i,j))


    print("basal indices", basal_indices)
    
    helices = []
    # complete
    for u, v in basal_indices:
        w = u 
        x = v

        while adj[w+1]==x-1 and w+1 < x-1:
            w+=1
            x-=1

        helices.append((u,v,w,x))

    return helices

helices = find_helices(dbn,adj)

f = open(snakemake.output[0], 'w')
for k, h in enumerate(helices):
    print("H"+str(k),h, file=f)

