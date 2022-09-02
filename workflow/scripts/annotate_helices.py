from minimal_expansion import MinimalExpansion

underlying_graph = MinimalExpansion()
dbn = open(snakemake.input.dbn).readlines()[0].rstrip('\n')
underlying_graph.from_str(dbn)

print(underlying_graph.helices)

f = open(snakemake.output[0], 'w')
for k, h in enumerate(underlying_graph.helices):
    print("H"+str(k),h, file=f)

