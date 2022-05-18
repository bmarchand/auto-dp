import sys
import copy
from utils import read_td_lines
from colors import *

colors = hex_Set3

# extracting bags and tree from td file
root = open(snakemake.input.tdname).readlines()[0].split(' ')[1].rstrip('\n')
adj, index2bag = read_td_lines(open(snakemake.input.tdname).readlines())


cluster_content = {}
which_cluster = {}
cluster_root = {}
cluster_extremities = {}
for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
    extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]
    cluster_extremities[label] = extremities

all_extremities = set([])

for key, val in cluster_extremities.items():
    all_extremities = all_extremities.union(set(val))

for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
    extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]

    queue = [('-1',root)]
    while len(queue) > 0:
        prev,u = queue.pop()

        if u.split('_')[0]==label:
            if not set(extremities).issubset(set(index2bag[prev])):
            # diag case
                keep_going = True
                while keep_going:
                    keep_going = False
                    for v in adj[u]:
                        if v.split('_')[0]==label:
                            for w in adj[v]:
                                if w!=u and w.split('_')[0] == label:
                                    # grand-child is still in helix, contracting v into u
                                    adj[u] = [bag for bag in adj[u] if bag!=v]+[w]
                                    adj[w] = [bag for bag in adj[w] if bag!=v]+[u]
                                    keep_going = True

        for v in adj[u]:
            if v!=prev:
                queue.append((u,v))

for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]
   
    cluster_content[label] = []
    extremities = [c.replace(' ','') for c in helixline.split('(')[1].split(')')[0].split(',')]
    cluster_extremities[label] = extremities

    queue = [('-1',root)]
    while len(queue) > 0:
        prev,u = queue.pop()
        print(label, u[:2], u) 
        if u.split('_')[0]==label:
            cluster_content[label].append(u)
            which_cluster[u] = label

            if set(extremities).issubset(set(index2bag[prev])):
            # clique case
                index2bag[u] = extremities
                adj[u] = []
            else:
            # diag case
                index2bag[u] = [vert for vert in index2bag[u] if vert in all_extremities]

        for v in adj[u]:
            if v!=prev:
                queue.append((u,v))

const_part = {}

for key, val in cluster_content.items():
    print("cluster content ",key, val)
    if len(val) > 0:
        const_part[key] = set.intersection(*[set(index2bag[u]) for u in val])
    else:
        const_part[key] = set([])

# adj, index2bag, const_part, which_cluster, cluster_root, cluster_extremities, all_extremities have been
# constructed

cnt = 0
f = open(snakemake.output[0],'w')

print('\\documentclass{article}',file=f)
print('\\begin{document}',file=f)

queue = [('-1',root)]

index2bag['-1'] = []

def num_to_letters(cnt):
    if cnt < 26:
        return chr(ord('a') + cnt).upper()
    else:
        return chr(ord('a') + int(cnt/26)).upper()+chr(ord('a') + int(cnt%26)).upper()

cnt = 0
bag_letter = {}

queue = [('-1',root)]

while len(queue) > 0:
    prev,u = queue.pop()
    if not u[:1]=='H':
        bag_letter[u] = num_to_letters(cnt)
        cnt += 1
    else:
        if set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
        # clique
            bag_letter[u] = 'CLIQUE'
        else:
        # diag
            if prev.split('_')[0]!=u.split('_')[0]:
                bag_letter[u] = num_to_letters(cnt)
                cnt += 1

    for v in adj[u]:
        if v!=prev:
            queue.append((u,v))

ext_to_letter = {}
for k, e in enumerate(sorted(list(all_extremities),key=lambda x: int(x))):
    ext_to_letter[e] = chr(ord('a')+k)

def partner(e, sorted_ext):
    if e==sorted_ext[0]:
        return sorted_ext[3]
    if e==sorted_ext[1]:
        return sorted_ext[2]
    if e==sorted_ext[3]:
        return sorted_ext[0]
    if e==sorted_ext[2]:
        return sorted_ext[1]

def subs(e, sorted_exs):
    if e==sorted_exs[0]:
        return sorted_exs[1]
    if e==sorted_exs[1]:
        return sorted_exs[0]
    if e==sorted_exs[2]:
        return sorted_exs[3]
    if e==sorted_exs[3]:
        return sorted_exs[2]

def increment(e, sorted_exs):
    if e==sorted_exs[0]:
        return '+1'
    if e==sorted_exs[1]:
        return '-1'
    if e==sorted_exs[2]:
        return '+1'
    if e==sorted_exs[3]:
        return '-1'



queue = [('-1',root)]
while len(queue) > 0:
    prev,u = queue.pop()
    if u[:1]=='H' and not set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
    # diag case
        if u.split('_')[0]!=prev.split('_')[0]:

            local_index_label = {}

            absent_ex = (set(cluster_extremities[which_cluster[u]])-set(index2bag[prev])).pop() 
            sorted_exs = sorted(cluster_extremities[which_cluster[u]], key=lambda x: int(x))
            
            indices = sorted(list(set(cluster_extremities[which_cluster[u]]) - set([absent_ex, partner(absent_ex, sorted_exs)])),key=lambda x: int(x))
            increments = [increment(e, sorted_exs) for e in indices]
            letters = [ext_to_letter[e] for e in indices]

            for i in indices:
                local_index_label[i] = ext_to_letter[i]
                local_index_label[subs(i, sorted_exs)] = ext_to_letter[i]

            const = []
            for e in sorted(const_part[which_cluster[u]], key=lambda x : int(x)):
                if e in indices:
                    const.append(ext_to_letter[e]+"'")
                    local_index_label[e] = ext_to_letter[e]+"'"
                else:
                    const.append(ext_to_letter[e])
                    local_index_label[e] = ext_to_letter[e]

            print('$$', bag_letter[u], '\\left[', file=f, end="")
            print(",".join(letters),"|",",".join(const),'\\right]',file=f, end="")
            print(' = \\min\\left(', file=f, end="")
            print(bag_letter[u]+'[',letters[0]+increments[0],',',letters[1]+'|'+",".join(const),'],', file=f, end="")
            print(bag_letter[u]+'[',letters[0],',',letters[1]+increments[1]+'|'+",".join(const),'],', file=f, end="")
            print(bag_letter[u]+'[',letters[0]+increments[0],',',letters[1]+increments[1]+'|'+",".join(const),']+bp('+letters[0]+','+letters[1]+')', file=f,end="")

            second_helix_bag = [v for v in adj[u] if v!=prev].pop()
            if len(adj[second_helix_bag]) >= 2:
                print(',',file=f,end="")
                child_table = [w for w in adj[second_helix_bag] if w!=u].pop()
                child_indices = sorted(index2bag[child_table], key=lambda x:int(x))
                child_indices = [i for i in child_indices if i in index2bag[second_helix_bag]]

                if child_table[0]=='H' and not set(cluster_extremities[which_cluster[child_table]]).issubset(set(index2bag[second_helix_bag])):
                # diag case below
                    absent_ex = (set(cluster_extremities[which_cluster[child_table]])-set(index2bag[second_helix_bag])).pop() 
                    sorted_exs = sorted(cluster_extremities[which_cluster[child_table]], key=lambda x: int(x))
                    child_indices = sorted(list(set(cluster_extremities[which_cluster[child_table]]) - set([absent_ex, partner(absent_ex, sorted_exs)])),key=lambda x: int(x))
                    child_letters = [local_index_label[i] for i in child_indices]
                    child_const = [local_index_label[i] for i in sorted(const_part[which_cluster[child_table]],key=lambda x : int(x))]
        
                    print(bag_letter[child_table]+'[',",".join(child_letters),'|',",".join(child_const),']',file=f, end="")

                else:
                # normal table below
                    child_letters = [local_index_label[i] for i in child_indices]
                    print(bag_letter[child_table]+'[',",".join(child_letters),']', file=f,end="")

            print('\\right)',file=f, end="")

            print('$$',file=f)

    elif u[:1]=='H' and set(cluster_extremities[which_cluster[u]]).issubset(set(index2bag[prev])):
    # clique case
        pass
    else: 

        indices = set(index2bag[u]).intersection(set(index2bag[prev]))
        new_vars = set(index2bag[u])-set(index2bag[prev])

        indices = [ext_to_letter[e] for e in sorted(list(indices),key=lambda x: int(x))]
        new_vars = [ext_to_letter[e] for e in sorted(list(new_vars),key=lambda x: int(x))]

        if len(indices)==0:
            print("$$",bag_letter[u], end=" ", file=f)
        else:
            print("$$",bag_letter[u]+'\\left[',",".join(indices),'\\right]',file=f,end = " ")
        
        if len(adj[u]) > 0:
            print("=\\min_{",",".join(new_vars),"}","\\left(",file=f , end=" ")
        
            terms = []

            for v in adj[u]:
                if v!=prev:
                    indices_v = set(index2bag[u]).intersection(set(index2bag[v]))
                    indices_v = [ext_to_letter[e] for e in sorted(list(indices_v),key=lambda x: int(x))]
                    terms.append(bag_letter[v]+'\\left['+",".join(indices_v)+'\\right]')
            print("+".join(terms), file=f, end="")


        print("\\right)", file=f, end=" ")

        print("$$", file =f)

        cnt += 1

    for v in adj[u]:
        if v!=prev:
            queue.append((u,v))

print('\\end{document}',file=f)
