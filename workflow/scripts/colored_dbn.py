from colors import *
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

f = open(snakemake.output[0],'w')

colors = Set3

print('\\documentclass{standalone}', file=f)
print('\\usepackage[x11names]{xcolor}', file=f)
print('\\usepackage{tikz}', file=f)
print('\\usepackage{relsize}', file=f)
print('\\begin{document}', file=f)

print('\\begin{tikzpicture}', file=f)

for k, c in enumerate(colors):
    print('\\definecolor{c'+str(k)+'}{rgb}{'+str(c)[1:-1]+'}',file=f)

dbn = open(snakemake.input.dbn).readlines()[0]

symbols = ['()','[]','{}','<>','Aa','Bb','Cc']

stacks = {}

for s in symbols:
    stacks[s] = []

edges = set([])
vertices =set([])

k = 0
int_label = {}
extremities_pos = [0]

dbn_list = list(dbn)
adj = {}

pos = 0
while len(dbn_list) > 0:
    int_label[k+1] = pos+1
    c = dbn_list.pop(0)
    vertices.add(k+1)

    if len(dbn_list) > 0:
        vertices.add((k+2))
        edges.add((k+1,k+2))
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
            edges.add((l, k+1))
            try:
                adj[k+1].append(l)
            except KeyError:
                adj[k+1] = [l]
            try:
                adj[l].append(k+1)
            except KeyError:
                adj[l] = [k+1]

    if len(dbn_list) > 0 and c==dbn_list[0]:
        pos += 1
    else:
        extremities_pos.append(k)
    k+= 1


helices = find_helices(adj)


for k, extremities in enumerate(helices):
    label = 'H'+str(k)

    i = int(extremities[0])-1 
    j = int(extremities[1])-1
    ip = int(extremities[2])-1
    jp = int(extremities[3])-1

    print('\\filldraw[fill=c'+str(int(label[1:])%len(colors))+',rounded corners] ', file=f, end="")
    print(' ('+str(i-0.2)+',-0.5) rectangle ('+str(ip+0.2)+',+0.5);', file=f)
    print('\\filldraw[fill=c'+str(int(label[1:])%len(colors))+',rounded corners] ', file=f, end="")
    print(' ('+str(jp-0.2)+',-0.5) rectangle ('+str(j+0.2)+',+0.5);', file=f)

def num_to_letters(cnt):
    if cnt < 26:
        return chr(ord('a') + cnt)
    else:
        return chr(ord('a') + int(cnt/26)).upper()+chr(ord('a') + int(cnt%26)).upper()


for k in range(len(vertices)-1):
    print("\\fill ("+str(k)+",0) circle (0.2) node[below=.5cm] {\\relsize{+1}{\\textbf{"+str(int_label[k+1])+"}}};", file=f)
all_extremities = set([])
for helixline in open(snakemake.input.helix).readlines():
    extremities = helixline.split(' ')[1][1:-1].split(',')
    all_extremities = all_extremities.union(set(extremities))
print(all_extremities)

import json
with open(snakemake.input.extremities_label) as ef:
    extremities_label = json.load(ef)

print(extremities_pos)
for k, e in enumerate(extremities_pos[:-1]):
    if k>0 and k <len(extremities_pos[:-1])-1:
        inc = 0.5
    else:
        inc = 0
    print(k, pos, chr(ord('a')+pos))
    print("\\fill ("+str(e+inc)+",0) circle (0.) node[below=1cm] {\\textbf{"+chr(ord('a')+k)+"}};", file=f)


for k in range(len(vertices)-2):
    print("\\draw[thick] ("+str(k)+",0) -- ("+str(k+1)+",0);", file=f )

for k,l in edges:
    if abs(k-l) <= 1:
        continue
    print("\\draw[very thick] ("+str(l-1)+",0) arc \
                (0:180:"+str(abs(0.5*(k-l)))+");",file=f)

print('\\end{tikzpicture}', file=f)
print('\\end{document}', file=f)
