
symbols = ['()','[]','{}','<>','Aa','Bb','Cc']

stacks = {}

for s in symbols:
    stacks[s] = []

dbn = open(snakemake.input[0]).readlines()[0].rstrip('\n')

vertices = set([])
edges = set([])

#for k,c in enumerate(dbn):
#    print(k,c)
#    vertices.add(k+1)
#    if k < len(dbn)-1:
#        edges.add((k+1,k+2))
#    for s in symbols:
#        if c==s[0]:
#            stacks[s].append(k+1)
#        if c==s[1]:
#            edges.add((stacks[s].pop(), k+1))

k = 0

dbn_list = list(dbn)

while len(dbn_list) > 0:
    c = dbn_list.pop(0)
    vertices.add(k+1)

    if len(dbn_list) > 0:
        edges.add((k+1,k+2))
        vertices.add((k+2))

    for s in symbols:
        if c==s[0]:
            stacks[s].append(k+1)
        if c==s[1]:
            edges.add((stacks[s].pop(), k+1))

    if len(dbn_list) > 0 and c==dbn_list[0]:
        k += 1


f = open(snakemake.output[0], 'w')

edges.add((1,k+1))

f.write('p tw '+str(len(vertices))+' '+str(len(edges))+'\n')
for u,v in edges:
    print(u,v,file=f)
