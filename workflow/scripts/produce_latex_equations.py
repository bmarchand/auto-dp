import sys
from equation_tree import TreeOfEquations
import copy
from utils import read_td_lines
from colors import *

colors = Set3

# extracting bags and tree from td file
tree_dec = TreeOfEquations()
print("init bag_content",tree_dec.bag_content)
tree_dec.read_from_file(snakemake.input.tdname)

print("after reading bag_content",tree_dec.bag_content)
# helices: sets a lot of useful variables
tree_dec.set_helices(open(snakemake.input.helix).readlines())

# extracting anchors
comp_key = lambda x : int(x)
print("after set helices bag_content",tree_dec.bag_content)
first_anchor = min([min([vertex for vertex in val], key=comp_key) for key, val in tree_dec.bag_content.items() if key!='-1'], key=comp_key)
last_anchor = max([max([vertex for vertex in val], key=comp_key) for key, val in tree_dec.bag_content.items() if key!='-1'], key=comp_key)

# contraction: 
tree_dec.contract_to_skeleton()

# filter to anchor vertices only
tree_dec.filter_anchors()

# tree_dec.bag_adj, tree_dec.bag_content, tree_dec.const_part, tree_dec.which_helix, cluster_root, tree_dec.cluster_extremities, all_extremities have been
# constructed

# LATEX_PREAMBULE BEGIN
f = open(snakemake.output[0],'w')

print('\\documentclass{article}', file=f)
print('\\usepackage[x11names]{xcolor}', file=f)
print('\\usepackage{amsmath}', file=f)
print('\\usepackage{graphicx}', file=f)
print('\\usepackage{amssymb}', file=f)
print('\\begin{document}', file=f)
print('\\textbf{fatgraph name: '+snakemake.wildcards.family+'}', file=f)

for k, c in enumerate(colors):
    print('\\definecolor{c'+str(k)+'}{rgb}{'+str(c)[1:-1]+'}',file=f)

print('\\begin{center}', file=f)
print('\\begin{figure}[h]', file=f)
print('\\includegraphics[width=\\textwidth]{'+snakemake.input.colored_dbn+'}', file=f)
print('\\end{figure}', file=f)
print('\\end{center}', file=f)

tree_dec.set_ext_to_letter()
print('ext to letter', tree_dec.ext_to_letter)
print('first and last anchors, already given: $',tree_dec.ext_to_letter[first_anchor]
                                                ,','
                                                ,tree_dec.ext_to_letter[last_anchor]
                                                ,'$'
                                                ,file=f)
# LATEX_PREAMBULE END

# giving a name and a color to each table
tree_dec.set_dp_table_names()

for prev,u in tree_dec.dfs_edge_iterator():
    if u[:1]=='H' and not set(tree_dec.helix_extremities[tree_dec.which_helix[u]]).issubset(set(tree_dec.bag_content[prev])):
    # diag case
        if u.split('-')[0]!=prev.split('-')[0]:

            equation = tree_dec.extract_diag_equation(prev, u)
            const = equation.constant_indices

            print('$$', tree_dec.dp_table_latex_snips[u]+"'", '\\left[', file=f, end="")
            print(",".join(equation.variable_indices),"|",",".join(const),'\\right]',file=f, end="")
            print(' =  \\min\\begin{cases}', file=f, end="")

            if not equation.inward:
                print(tree_dec.dp_table_latex_snips[u]+"'"+'[',
                      equation.variable_indices[0]+equation.increments[0],
                      ',',
                      equation.variable_indices[1]+'|'+",".join(const),
                      '], &\\text{if }',
                      equation.variable_indices[0]+equation.increments[0],
                      '\\notin\{',equation.variable_indices[1],
                      ",",
                      ",".join(const),
                      '\}',
                      '\\\\', 
                      file=f, end="")
            else:
                print(tree_dec.dp_table_latex_snips[u]+"'"+'[',
                      equation.variable_indices[0],
                      ',',
                      equation.variable_indices[1]+equation.increments[1]+'|'+",".join(const),
                      '], &\\text{if }',
                      equation.variable_indices[1]+equation.increments[1],
                      ',\\notin\{',
                      equation.variable_indices[0],
                      ",",
                      ",".join(const),
                      '\}',
                      '\\\\', 
                      file=f, end="")

            print(tree_dec.dp_table_latex_snips[u]+'[',
                  equation.variable_indices[0]+equation.increments[0],
                  ',',
                  equation.variable_indices[1]+equation.increments[1]+'|'+",".join(const),
                  ']+\\Delta G('+equation.variable_indices[0]+','+equation.variable_indices[1]+') &\\text{if }',
                  '\{',equation.variable_indices[0]+equation.increments[0],
                  ',',
                  equation.variable_indices[1]+equation.increments[1],
                  '\}\\cap',
                  '\{',
                  ",".join(const),'\}=\\emptyset', file=f,end="")

            print('\\end{cases}',file=f, end="")
            print('$$',file=f)
            
            print('$$', tree_dec.dp_table_latex_snips[u], '\\left[', file=f, end="")
            print(",".join(equation.variable_indices),"|",",".join(const),'\\right]',file=f, end="")
            print(' =  \\min\\begin{cases}', file=f, end="")

            if equation.inward:

                print(tree_dec.dp_table_latex_snips[u]+'[',
                      equation.variable_indices[0]+equation.increments[0],
                      ',',equation.variable_indices[1]+'|'+",".join(const),
                      '], &\\text{if }',
                      equation.variable_indices[0]+equation.increments[0],
                      '\\notin\{',equation.variable_indices[1],
                      ",",
                      ",".join(const),
                      '\}','\\\\', file=f, end="")

            else:
                print(tree_dec.dp_table_latex_snips[u]+'[',
                      equation.variable_indices[0],
                      ',',equation.variable_indices[1]+equation.increments[1]+'|'+",".join(const),
                      '], &\\text{if }',
                      equation.variable_indices[1]+equation.increments[1],
                      ',\\notin\{',
                      equation.variable_indices[0],
                      ",",
                      ",".join(const),'\}','\\\\', file=f, end="")

            if not equation.inward:
                print(tree_dec.dp_table_latex_snips[u]+"'"+'[',
                      equation.variable_indices[0]+equation.increments[0],
                      ',',
                      equation.variable_indices[1]+'|'+",".join(const),
                      '], &\\text{if }',
                      equation.variable_indices[0]+equation.increments[0],
                      '\\notin\{',equation.variable_indices[1],
                      ",",",".join(const),'\}','\\\\', file=f, end="")

            else:
                print(tree_dec.dp_table_latex_snips[u]+"'"+'[',
                      equation.variable_indices[0],
                      ',',
                      equation.variable_indices[1]+equation.increments[1]+'|'+",".join(const),
                      '], &\\text{if }',equation.variable_indices[1]+equation.increments[1],
                      ',\\notin\{',equation.variable_indices[0],
                      ",",
                      ",".join(const),'\}','\\\\', file=f, end="")

            print(tree_dec.dp_table_latex_snips[u]+'[',
                  equation.variable_indices[0]+equation.increments[0],
                  ',',
                  equation.variable_indices[1]+equation.increments[1]+'|'+",".join(const),
                  ']+\\Delta G('+equation.variable_indices[0]+','+equation.variable_indices[1]+') &\\text{if }',
                  '\{',
                  equation.variable_indices[0]+equation.increments[0],
                  ',',
                  equation.variable_indices[1]+equation.increments[1],
                  '\}\\cap',
                  '\{',
                  ",".join(const),'\}=\\emptyset', file=f,end="")

            if len(tree_dec.bag_adj[equation.second_bag]) >= 2:
                print(',\\\\',file=f,end="")
                print('+'.join(sub_terms),end="",file=f)

            print('\\end{cases}',file=f, end="")

            print('$$',file=f)

    elif u[:1]=='H' and set(tree_dec.helix_extremities[tree_dec.which_helix[u]]).issubset(set(tree_dec.bag_content[prev])):
    # clique case
        pass
    else: 

        indices = set(tree_dec.bag_content[u]).intersection(set(tree_dec.bag_content[prev]))
        new_vars = set(tree_dec.bag_content[u])-set(tree_dec.bag_content[prev])
#        new_vars -= set([first_anchor])
#        new_vars -= set([last_anchor])

        indices = [tree_dec.ext_to_letter[e] for e in sorted(list(indices),key=lambda x: int(x))]
        new_vars = [tree_dec.ext_to_letter[e] for e in sorted(list(new_vars),key=lambda x: int(x))]

        if len(indices)==0:
            print("$$",tree_dec.dp_table_latex_snips[u], end=" ", file=f)
        else:
            print("$$",tree_dec.dp_table_latex_snips[u]+'\\left[',",".join(indices),'\\right]',file=f,end = " ")
        
        if len(set(tree_dec.bag_adj[u])-set([prev])) > 0:
            print("=\\min_{",",".join(new_vars),"}","\\left(",file=f , end=" ")
        
            terms = []

            for v in tree_dec.bag_adj[u]:
                if v!=prev:
                    if v[:1]=='H' and not set(tree_dec.helix_extremities[tree_dec.which_helix[v]]).issubset(set(tree_dec.bag_content[u])):
            
                        # diag bag
                        equation = tree_dec.extract_diag_equation(u, v)
                        terms.append(tree_dec.dp_table_latex_snips[v]+'\\left['+",".join(equation.variable_indices)+"|"+",".join(equation.constant_indices)+'\\right]')

                    elif v[:1]=='H' and set(tree_dec.helix_extremities[tree_dec.which_helix[v]]).issubset(set(tree_dec.bag_content[u])):
                        indices_v = set(tree_dec.bag_content[u]).intersection(set(tree_dec.bag_content[v]))
                        indices_v = [tree_dec.ext_to_letter[e] for e in sorted(list(indices_v),key=lambda x: int(x))]
                        indices_v[1] = indices_v[1]+'-1'
                        indices_v[3] = indices_v[3]+'-1'
                        terms.append(tree_dec.dp_table_latex_snips[v]+'\\left['+",".join(indices_v)+'\\right]')

                    else:
                        #normal bag
                        indices_v = set(tree_dec.bag_content[u]).intersection(set(tree_dec.bag_content[v]))
                        indices_v = [tree_dec.ext_to_letter[e] for e in sorted(list(indices_v),key=lambda x: int(x))]
                        terms.append(tree_dec.dp_table_latex_snips[v]+'\\left['+",".join(indices_v)+'\\right]')
            print("+".join(terms), file=f, end="")


        print("\\right)", file=f, end=" ")

        print("$$", file =f)

#print('$$',end=" ",file=f)
#print("C_\\boxtimes'[i,i',j',j]=\\begin{cases} ",file=f,end=" ")
#print("C_\\boxtimes'[i,i',j',j-1] \\\\",file=f)
#print("C_\\boxtimes[i+1,i',j',j-1] + \\Delta G(i,j) \\\\",file=f)
#print("\\Delta G(i,j) \\\\",file=f)
#print('\\end{cases}',file=f)
#print('$$',end=" ",file=f)
#
#print('$$',end=" ",file=f)
#print('C_\\boxtimes=\\begin{cases}',file=f,end=" ")
#
#print('end{cases}',file=f)
#print('$$',end=" ",file=f)


print('\\end{document}',file=f)
