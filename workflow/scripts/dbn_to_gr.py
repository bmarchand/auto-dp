
symbols = ['()','[]','{}','<>','Aa','Bb','Cc']

stacks = {}

for s in symbols:
    stacks[s] = []

dbn = open(snakemake.input[0]).readlines()[0].rstrip('\n')

vertices = set([])
edges = set([])

for k,c in enumerate(dbn):
    print(k,c)
    vertices.add(k+1)
    if k < len(dbn)-1:
        edges.add((k+1,k+2))
    for s in symbols:
        if c==s[0]:
            stacks[s].append(k+1)
        if c==s[1]:
            edges.add((stacks[s].pop(), k+1))

f = open(snakemake.output[0], 'w')

#edges.add((1,len(dbn)))

f.write('p tw '+str(len(vertices))+' '+str(len(edges))+'\n')
for u,v in edges:
    print(u,v,file=f)
