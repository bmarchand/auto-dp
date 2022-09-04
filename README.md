# auto-dp

This repository contains proof-of-concept code for the methods described our [WABI 2022 paper](https://hal.inria.fr/hal-03676377).
It consists of a **snakemake** workflow, that is capable of producing various types of output files (latex equations, visualizations...)
given a user-specified input file.

As described in the paper, the output latex equations are for a DP scheme solving the folding problem restricted to the family
of RNA structures specified by an input fatgraph. This input fatgraph needs to be written in a file in a specific 
directory of the repository, while the outputs are then generated with snakemake terminal commands.

## Dependencies

The following are needed to execute the snakemake pipeline:

- [snakemake](https://snakemake.readthedocs.io/en/stable/).

- a Java compiler for the [meiji](https://github.com/TCS-Meiji/PACE2017-TrackA) tree decomposition solver (source code included in this repo under `workflow/scripts/PACE2017-TrackA`, see compilation section below).

- a TeX distribution (capable of executing pdflatex commands).

This code was developed on a Linux machine. As snakemake will execute commands in the terminal directly,
the commands must be execute on a **Unix-like** terminal in order to work.

## How to use

Imagine you are interested in the following kissing-hairpins pattern: ``([)(])``.

Such a string will describe a fatgraph in which each base pair is seen as an helix of arbitrary length.
It needs to be written in a one-line file called, for instance, `khp.dbn` and located under `resources/dbn_files`.

Latex equations such as the ones presented in our paper can then be produced with:

```
snakemake -c1 results/latex_equations/khp_latex_equations.pdf
```

Given this command, snakemake will look for rules to produce ``results/latex_equations/khp_latex_equations.pdf``.
It will see that it is capable of producing `results/latex_equations/{name}_latex_equations.pdf` given (with a few steps in between) `resources/dbn_files/{name}.dbn`.

## Meiji solver compilation

```
cd workflow/scripts/PACE2017-TrackA/
javac tw/exact/*.java
```
