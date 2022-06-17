symbols = ["<>","()","[]","{}","Aa","Bb","Cc","Dd"]

stacks = {}

for s in symbols:
    stacks[s] = []

adj = {}

dbn = open(snakemake.input[0]).readlines()[0]
k = 0

dbn_list = list(dbn)

while len(dbn_list) > 0:
    c = dbn_list.pop(0)

    if len(dbn_list) > 0:
        try:
            adj[k+1].append(k+2)
        except KeyError:
            adj[k+1] = [k+2]
        try:
            adj[k+2].append(k+1)
        except KeyError:
            adj[k+2] = [k+1]
     
    for s in symbols:
        if c==s[0]:
            stacks[s].append(k+1)
        if c==s[1]:
            l = stacks[s].pop()
            try:
                adj[k+1].append(l)
            except KeyError:
                adj[k+1] = [l]
            try:
                adj[l].append(k+1)
            except KeyError:
                adj[l] = [k+1]

    if len(dbn_list) > 0 and c==dbn_list[0]:
        k += 1


def find_helices(adj):

    # basal indices (largest overarching arc)
    basal_indices = []

    for i in range(1, max(adj.keys())+1,1):
        for j in range(i+1, max(adj.keys())+1,1):
            if j in adj[i] and abs(j-i) > 1:
                try:
                    if j+1 in adj[i-1]:
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
        while x-1 in adj[w+1] and w+1 < x-1:
            w+=1
            x-=1

        helices.append((u,v,w,x))

    return helices

print(adj)
helices = find_helices(adj)

f = open(snakemake.output[0], 'w')
for k, h in enumerate(helices):
    print("H"+str(k),h, file=f)

