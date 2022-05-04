import sys

colors = ["lime","pink","cyan","olive","orange","gray"] 
#colors = ["burlywood","plum","skyblue","seagreen","coral","wheat"] 


# extracting bags and tree from td file
index2bag = {}
adj = {}

started_bs = False

for line in open(snakemake.input.tdname).readlines():
    if line[0]=='b':
        started_bs = True
        index2bag[line.split(' ')[1].replace('-','_')] = [vertex.rstrip('\n') for vertex in line.split(' ')[2:-1]]

    else:
        if started_bs:
            i = line.split(' ')[0].replace('-','_')
            j = line.split(' ')[1].rstrip('\n').replace('-','_')
            try:
                adj[i].append(j)
            except KeyError:
                adj[i] = [j]
            try:
                adj[j].append(i)
            except KeyError:
                adj[j] = [i]

root = list(adj.keys())[0]

f = open(snakemake.output[0],'w')

f.write('digraph G {\n')
print("    node [shape=box];",file=f)
subgraph = {}
cluster_content = {}
which_cluster = {}
cluster_root = {}
cluster_extremities = {}
for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
   
    cluster_content[label] = []
    extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]
    cluster_extremities[label] = extremities

    subgraph[label] = ""
    queue = [('-1','1')]
    while len(queue) > 0:
        prev,u = queue.pop()
        print(label, u[:2], u) 
        if u.split('_')[0]==label:
            cluster_content[label].append(u)
            which_cluster[u] = label
            if len(subgraph[label]) > 0:
                subgraph[label] += ' -> '
                subgraph[label] += u
            else:
                cluster_root[label] = prev
                subgraph[label] += u

        for v in adj[u]:
            if v!=prev:
                queue.append((u,v))

    subgraph[label] += ';'
    if subgraph[label]==';':
        subgraph.pop(label)

const_part = {}

for key, val in cluster_content.items():
    print("cluster content ",key, val)
    if len(val) > 0:
        const_part[key] = set.intersection(*[set(index2bag[u]) for u in val])
    else:
        const_part[key] = set([])

cnt = 0
def color(u):
    return colors[int(u.split('_')[0][1:])%len(colors)]
for key, val in subgraph.items():
    print("    subgraph cluster"+str(cnt)+' {',file=f)
    print("        node [style=filled,fillcolor=white];",file=f)
    print('        labeljust="l";',file=f)
    print("        style=filled;",file=f)
    print("        color="+colors[int(key[1:])%len(colors)]+";",file=f)
    print("        "+val,file=f)
    print(key,set(cluster_extremities[key]))
    print(set(index2bag[cluster_root[key]]))
    if set(cluster_extremities[key]).issubset(set(index2bag[cluster_root[key]])) :
        case = ' (clique)'
    else:
        case = ' (diag)'
    print(case)
    ext = " ("
    for c in sorted(cluster_extremities[key],key=lambda x:int(x)):
        ext += c +"-"
    ext = ext[:-1]
    ext += ')'
    print('        label="'+key+ext+case+'";',file=f)
    print("    }",file=f)
    cnt += 1

queue = [('-1','1')]


def color(u):
    return colors[int(u.split('_')[0][1:])%len(colors)]

all_extremities = set([])

def boldified(c, all_extremities):
    if c in all_extremities:
        return "<b>"+c+"</b>"
    else:
        return c

for key, val in cluster_extremities.items():
    all_extremities = all_extremities.union(set(val))

while len(queue) > 0:
    prev,u = queue.pop()
    label = "<{"
    if u[:1]=='H':
        print(index2bag[u])
        print(const_part[which_cluster[u]])
        label+=''
        for c in set(index2bag[u])-const_part[which_cluster[u]]:
            label += " "+boldified(c, all_extremities)
        label += "| "
        for c in const_part[which_cluster[u]]:
            label += " "+boldified(c, all_extremities)

    else:
        for c in index2bag[u]:
            label += " "+boldified(c, all_extremities)
#    if u[0]=='H':
#        print(u,color(u))
#        print("    ",u,'[color="'+color(u)+'",style=filled,label="',label,'"];', file=f)
#    else:
    label += "}>"
    print("    ",u,'[shape=record,label=',label,'];', file=f)
    if u.split('_')[0]!=prev.split('_')[0]:
        print("    ",prev," -> ",u+';',file=f)

    for v in adj[u]:
        if v!=prev:
            queue.append((u,v))


print('}',file=f)
