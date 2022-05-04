colors = ["lime","pink","cyan","olive","orange","gray"] 

f = open(snakemake.output[0],'w')

print('\\documentclass{standalone}', file=f)
print('\\usepackage[x11names]{xcolor}', file=f)
print('\\usepackage{tikz}', file=f)
print('\\begin{document}', file=f)

print('\\begin{tikzpicture}', file=f)

dbn = open(snakemake.input.dbn).readlines()[0]


symbols = ['()','[]','{}','<>','Aa','Bb','Cc']

stacks = {}

for s in symbols:
    stacks[s] = []

edges = set([])

for k,c in enumerate(dbn):
    print(k,c)
    if k < len(dbn)-1:
        edges.add((k+1,k+2))
    for s in symbols:
        if c==s[0]:
            stacks[s].append(k+1)
        if c==s[1]:
            edges.add((stacks[s].pop(), k+1))


for helixline in open(snakemake.input.helix).readlines():
    label = helixline.split(' ')[0]

    extremities = helixline.split('(')[1].split(')')[0].split(',')

    i = int(extremities[0])-1 
    j = int(extremities[1])-1
    ip = int(extremities[2])-1
    jp = int(extremities[3])-1

    print("label, color", label,colors[int(label[1:])%len(colors)]) 
    print('\\filldraw[fill='+colors[int(label[1:])%len(colors)]+',rounded corners] ', file=f, end="")
    print(' ('+str(i-0.2)+',-0.5) rectangle ('+str(ip+0.2)+',+0.5);', file=f)
    print('\\filldraw[fill='+colors[int(label[1:])%len(colors)]+',rounded corners] ', file=f, end="")
    print(' ('+str(jp-0.2)+',-0.5) rectangle ('+str(j+0.2)+',+0.5);', file=f)

for k in range(len(dbn)-1):
    print("\\fill ("+str(k)+",0) circle (0.2) node[below=.5cm] {\\textbf{"+str(k+1)+"}};", file=f)

for k in range(len(dbn)-2):
    print("\\draw[thick] ("+str(k)+",0) -- ("+str(k+1)+",0);", file=f )

for k,l in edges:
    if abs(k-l) <= 1:
        continue
    print("\\draw[very thick] ("+str(l-1)+",0) arc \
                (0:180:"+str(abs(0.5*(k-l)))+");",file=f)

print('\\end{tikzpicture}', file=f)

print('\\end{document}', file=f)
