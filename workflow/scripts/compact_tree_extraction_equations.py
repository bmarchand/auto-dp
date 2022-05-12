import sys
import copy
Paired = ['#A6CEE3', '#1F78B4', '#B2DF8A', '#33A02C', '#FB9A99', '#E31A1C', '#FDBF6F', '#FF7F00', '#CAB2D6', '#6A3D9A', '#FFFF99', '#B15928']
Accent = ['#7FC97F', '#BEAED4', '#FDC086', '#FFFF99', '#386CB0', '#F0027F', '#BF5B16', '#666666']
Dark2 = ['#1B9E77', '#D95F02', '#7570B3', '#E7298A', '#66A61E', '#E6AB02', '#A6761D', '#666666']
Set1 = ['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3', '#FF7F00', '#FFFF33', '#A65628', '#F781BF', '#999999']
Set2 = ['#66C2A5', '#FC8D62', '#8DA0CB', '#E78AC3', '#A6D854', '#FFD92F', '#E5C494', '#B3B3B3']
Set3 = ['#8DD3C7', '#FFFFB3', '#BEBADA', '#FB8072', '#80B1D3', '#FDB462', '#B3DE69', '#FCCDE5', '#D9D9D9', '#BC80BD', '#CCEBC5', '#FFED6F']
tab10 = ['#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF']
tab20 = ['#1F77B4', '#AEC7E8', '#FF7F0E', '#FFBB78', '#2CA02C', '#98DF8A', '#D62728', '#FF9896', '#9467BD', '#C5B0D5', '#8C564B', '#C49C94', '#E377C2', '#F7B6D2', '#7F7F7F', '#C7C7C7', '#BCBD22', '#DBDB8D', '#17BECF', '#9EDAE5']
tab20b = ['#393B79', '#5254A3', '#6B6ECF', '#9C9EDE', '#637939', '#8CA252', '#B5CF6B', '#CEDB9C', '#8C6D31', '#BD9E39', '#E7BA52', '#E7CB94', '#843C39', '#AD494A', '#D6616B', '#E7969C', '#7B4173', '#A55194', '#CE6DBD', '#DE9ED6']
tab20c = ['#3182BD', '#6BAED6', '#9ECAE1', '#C6DBEF', '#E6550D', '#FD8D3C', '#FDAE6B', '#FDD0A2', '#31A354', '#74C476', '#A1D99B', '#C7E9C0', '#756BB1', '#9E9AC8', '#BCBDDC', '#DADAEB', '#636363', '#969696', '#BDBDBD', '#D9D9D9']

colors = Set3
from utils import read_td_lines, full_compact_diag, full_compact_clique, subgraph_info_extraction

# extracting bags and tree from td file
adj, index2bag = read_td_lines(open(snakemake.input.tdname).readlines())

# extracting extremities
cluster_extremities = {}
for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
    extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]
    cluster_extremities[label] = extremities

all_extremities = set([])

for key, val in cluster_extremities.items():
    all_extremities = all_extremities.union(set(val))

# for all helices, contraction to one bag (the highest in the tree)
for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
    extremities = cluster_extremities[label]

    adj, index2bag = full_compact_diag(label, extremities, adj, index2bag)
    adj, index2bag = full_compact_clique(label, extremities, adj, index2bag)

# for all helices: building the colored box around it
subgraph = {}
cluster_content = {}
cluster_root = {}

# which cluster filling
which_cluster = {}
for u in index2bag.keys():
    if u[0]=='H':
        which_cluster[u] = u.split('_')[0]

# subgraph constructions
for helixline in open(snakemake.input.helix).readlines():

    label = helixline.split(' ')[0]
    subgraph_string, content, root = subgraph_info_extraction(label, adj)

    if subgraph_string!=';':
        subgraph[label] = subgraph_string
    cluster_content[label] = content
    cluster_root[label] = root

const_part = {}

for key, val in cluster_content.items():
    print("cluster content ",key, val)
    if len(val) > 0:
        const_part[key] = set.intersection(*[set(index2bag[u]) for u in val])
    else:
        const_part[key] = set([])


# STARTING TO WRITE OUTPUT DOT FILE
f = open(snakemake.output[0],'w')

f.write('digraph G {\n')
print("    node [shape=box];",file=f)

cnt = 0
for key, val in subgraph.items():
    color = colors[int(key[1:])]
    if set(cluster_extremities[key]).issubset(set(index2bag[cluster_root[key]])) :
        case = ' (clique)'
    else:
        case = ' (diag)'
    print("val", val)
    print("    subgraph cluster"+str(cnt)+' {',file=f)
    print("        node [style=filled,fillcolor=white];",file=f)
    print('        labeljust="l";',file=f)
    print("        style=filled;",file=f)
    print('        color="'+color+'";',file=f)
    print("        "+val,file=f)
    print(key,set(cluster_extremities[key]))
    print(set(index2bag[cluster_root[key]]))
    ext = " ("
    for c in sorted(cluster_extremities[key],key=lambda x:int(x)):
        ext += c +"-"
    ext = ext[:-1]
    ext += ')'
    print('        label="'+key+ext+case+'";',file=f)
    print("    }",file=f)
    cnt += 1


def rank(c,all_extremities):
    for k, val in enumerate(sorted(list(all_extremities), key=lambda x: int(x))):
        if val==c:
            return k

def boldified(c, all_extremities, inc=None):
    if c in all_extremities:
        if inc:
            return "<b>"+chr(ord('a')+rank(c, all_extremities))+inc+"</b>"
        else:
            return "<b>"+chr(ord('a')+rank(c, all_extremities))+"</b>"
    else:
        return c
index2bag['-1'] = []

def num_to_letters(cnt):
    if cnt < 26:
        return chr(ord('a') + cnt).upper()
    else:
        return chr(ord('a') + int(cnt/26)).upper()+chr(ord('a') + int(cnt%26)).upper()

cnt = 0

bag_letter = {}

queue = [('-1','1')]

while len(queue) > 0:
    prev,u = queue.pop()
    if not u[:1]=='H':
        bag_letter[u] = '<FONT COLOR="RED"><b>'+num_to_letters(cnt)+'</b></FONT>'
        cnt += 1
    else:
        if set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
        # clique
            bag_letter[u] = '<FONT COLOR="RED"><b>'+'CLIQUE'+'</b></FONT>'
        else:
        # diag
            bag_letter[u] = '<FONT COLOR="RED"><b>'+'DIAG'+'</b></FONT>'

    for v in adj[u]:
        if v!=prev:
            queue.append((u,v))

queue = [('-1','1')]

while len(queue) > 0:
    prev,u = queue.pop()
    label = "<{"
    if u[:1]=='H' and not set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
    # diag case
#        label += '  <FONT COLOR="RED"><b>'+num_to_letters(cnt)+'</b></FONT>'

        
        label += bag_letter[u]+'['
        e1, e2 = tuple(set(index2bag[u]).intersection(set(cluster_extremities[which_cluster[u]])))
        if int(e1) > int(e2):
            e1, e2 = e2, e1
        label += boldified(e1,all_extremities)+','
        label += boldified(e2,all_extremities)+'\|'
        for c in set(index2bag[u]):
            if c not in cluster_extremities[which_cluster[u]]:
                label += boldified(c, all_extremities)+','
        label = label[:-1]+'] = min('

        # inward or outward ?
        if max([int(e) for e in cluster_extremities[which_cluster[u]]]) in [e1,e2]:
            inc1 = '+1'
            inc2 = '-1'
        else:
            inc1 = '-1'
            inc2 = '+1'
            

        label += bag_letter[u]+'['+boldified(e1,all_extremities,inc=inc1)+','
        label += boldified(e2, all_extremities)+'\|'
        for c in sorted(index2bag[u],key=lambda x:int(x)):
            if c not in cluster_extremities[which_cluster[u]]:
                label += boldified(c, all_extremities)+','
        label = label[:-1]+']'

        label += ','
        label += bag_letter[u]+'['+boldified(e1,all_extremities)+','
        label += boldified(e2, all_extremities,inc=inc2)+'\|'
        for c in sorted(index2bag[u],key=lambda x:int(x)):
            if c not in cluster_extremities[which_cluster[u]]:
                label += boldified(c, all_extremities)+','
        label = label[:-1]+']'
        
        # base pair
        label += ','
        label += bag_letter[u]+'['+boldified(e1,all_extremities,inc=inc1)+','
        label += boldified(e2, all_extremities,inc=inc2)+':'
        for c in sorted(index2bag[u],key=lambda x:int(x)):
            if c not in cluster_extremities[which_cluster[u]]:
                label += boldified(c, all_extremities)+','
        label = label[:-1]+']+BP('+boldified(e1, all_extremities)+','+boldified(e2,all_extremities)+'), '

        for v in adj[u]:
            if v!=prev:
                label += bag_letter[v]+'['
                for c in sorted(list(set(index2bag[v]).intersection(set(index2bag[u]))), key= lambda x:int(x)):
                    label+=boldified(c,all_extremities)+','
                label=label[:-1]+']'

        label+=')'

    elif u[:1]=='H' and set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
    # clique case
        label += bag_letter[u]+'['
        for c in sorted(index2bag[u],key=lambda x:int(x)):
            label += boldified(c, all_extremities)+','
        label = label[:-1]+'].'

    else: 
    # other bags
        if prev!='-1':
            label += bag_letter[u]+'['

            for c in sorted(index2bag[u],key=lambda x:int(x)):
                if c in set(index2bag[u]).intersection(set(index2bag[prev])):
                    label += boldified(c, all_extremities)+','
            label = label[:-1]+'] =min_('
        else:
            label +='min_('
        for c in sorted(index2bag[u],key=lambda x: int(x)):
            if c not in set(index2bag[u]).intersection(set(index2bag[prev])):
                if str(int(c)-1) in set(index2bag[u]).intersection(set(index2bag[prev])):
                    label += boldified(str(int(c)-1), all_extremities)+' &le;'
                label += '<FONT COLOR="DARKGREEN">'+boldified(c, all_extremities)+'</FONT> &le;'
                if str(int(c)+1) in set(index2bag[u]).intersection(set(index2bag[prev])):
                    label += boldified(str(int(c)+1), all_extremities)+' &le;'

        label =label[:-4]+') ('
        for v in adj[u]:
            if v!=prev:
                label += bag_letter[v]+'['
                for c in sorted(list(set(index2bag[v]).intersection(set(index2bag[u]))), key= lambda x:int(x)):
                    label+=boldified(c,all_extremities)+','
                label=label[:-1]+']+'

        label = label[:-1]+')'


    label += "}>"
    print("    ",u,'[shape=record,label=',label,'];', file=f)
    if u.split('_')[0]!=prev.split('_')[0]:
        print("    ",prev," -> ",u+';',file=f)

    for v in adj[u]:
        if v!=prev:
            queue.append((u,v))

label = "<{"
for c in sorted(list(all_extremities),key=lambda x:int(x)):
    label += boldified(c,all_extremities)
    label += '=&#956;('+c+')'+' | '
label += "}>"

print("    labels",'[shape=record,label=',label,'];', file=f)

print('}',file=f)
