from autodp.equation_tree import TreeOfEquations, BagType

# extracting bags and tree from td file
tree_dec = TreeOfEquations()
tree_dec.read_from_file(snakemake.input.tdname)

# helices: sets a lot of useful variables
tree_dec.set_helices(open(snakemake.input.helix).readlines())

# contraction: 
tree_dec.contract_to_skeleton()

# filter to anchor vertices only
tree_dec.filter_anchors()

# start file
f = open(snakemake.output[0],'w')

print('#include <stdio.h>', file = f)
print('#include <stdlib.h>', file = f)
print("int main(int argc, char ** argv) {", file=f)
print("    char * line = NULL;", file=f)
print("    size_t len = 0;", file=f)
print('    FILE * fp = fopen(argv[1], "r");', file=f)
print("    if (fp == NULL)", file=f)
print("        exit(EXIT_FAILURE);", file=f)
print("    while( getline(&line, &len, fp)!=-1) {", file=f)
print('        printf("%s", line);', file=f)
print('        char * struct = fold(line);', file=f)
print('        printf("%s", struct);', file=f)
print("    }", file=f)
print("}", file=f)
