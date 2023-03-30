#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>

int min(int a, int b) { if (a<b) {return a;} else {return b;}};

int index_B(int a,int d,int d2,int e);
int index_CLIQUE(int i, int j, int k, int l);

void init_fill_B();
void init_fill_CLIQUE();

int compute_A();
int compute_B(int a,int d,int d2,int e);
int compute_B2(int a,int d,int d2,int e);
int fold();

int n;

char * line = NULL;

double * B;
double * B2;
double * CLIQUE;
double * CLIQUE2;

int main(int argc, char ** argv) {
    char * line = NULL;
    size_t len = 0;
    FILE * fp = fopen(argv[1], "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    getline(&line, &len, fp); 
    printf("%s", line);
    double * B = malloc(n*n*n*n*sizeof(double));
double * B2 = malloc(n*n*n*n*sizeof(double));
    double * CLIQUE = malloc(n*n*n*n*sizeof(double));
    init_fill_B();
    init_fill_CLIQUE();
    int score = fold();
    free(B);
    free(CLIQUE);
}
int fold() {
    compute_A();
    }

int compute_CLIQUE2(int i, int j, int k, int l);

int bp_score(char x, char y) {
    if (x=='G' && y=='C') { return 10; }
    if (x=='C' && y=='G') { return 10; }
    if (x=='G' && y=='U') { return 5; }
    if (x=='U' && y=='G') { return 5; }
    if (x=='A' && y=='U') { return 5; }
    if (x=='U' && y=='A') { return 5; }
    return 0;
}

int compute_CLIQUE(int i, int j, int k, int l) {
    //C_boxtimes in article"
    if (CLIQUE[index_CLIQUE(i,j,k,l)] > INT_MIN) { 
        return CLIQUE[index_CLIQUE(i,j,k,l)];
    }
    
    int min_value = INT_MAX;

    if (k < l) { 
        min_value = min(min_value, compute_CLIQUE2(i,j,k,l-1)); 
    }
    if (i < j) {
        min_value = min(min_value, compute_CLIQUE(i+1,j,k,l));
    }
    if (i < j && k < l) {
        min_value = min(min_value, 
                    compute_CLIQUE(i+1, j, k, l-1)+bp_score(line[i],line[l]));
    }
    if (k==l) { 
        min_value = min(min_value, bp_score(line[i], line[l]));
    }

    CLIQUE[index_CLIQUE(i,j,k,l)] = min_value;
    return min_value;
}

int compute_CLIQUE2(int i, int j, int k, int l) {
    //C_boxtimes' in article:w

    if (CLIQUE2[index_CLIQUE(i,j,k,l)] > INT_MIN) { 
        return CLIQUE2[index_CLIQUE(i,j,k,l)];
    }
    int min_value = INT_MAX;

    if (k < l) { 
        min_value = min(min_value, compute_CLIQUE2(i,j,k,l-1)); 
    }
    if (i < j && k < l) {
        min_value = min(min_value, 
                    compute_CLIQUE(i+1, j, k, l-1)+bp_score(line[i],line[l]));
    }
    if (k==l) { 
        min_value = min(min_value, bp_score(line[i], line[l]));
    }

    CLIQUE2[index_CLIQUE(i,j,k,l)] = min_value;
    return min_value;
}
void init_fill_B() {
    for (int a=0;a<n;a++) {
        for (int d=a;d<n;d++) {
            for (int d=d;d<n;d++) {
                for (int e=d;e<n;e++) {
                    B[index_B(a,d,d,e)] = INT_MIN;
                }
            }
        }
    }
}

int index_B(int a,int d,int d2,int e)  {
    return n*n*n*a+n*n*d+n*d2+e;
}

void init_fill_CLIQUE() {
    for (int i=0; i < n;i++) {
        for (int j=i; j < n;j++) {
            for (int k=j; k < n;k++) {
                for (int l=k; l < n;l++) {
                    CLIQUE[i,j,k,l] = INT_MIN;
                }
            }
        }
    }
}
int index_CLIQUE(int i, int j, int k, int l) {
    return n*n*n*i+n*n*j+n*k+l;
}

int compute_A() {
    
    int min_value = INT_MAX;
    
    for (int a=0;a<n;a++) {
        for (int d=a;d<n;d++) {
            for (int e=d;e<n;e++) {
                min_value = min(min_value, compute_B(a,d,d,e));
            }
        }
    }

    return min_value;
}

int compute_B(int a, int d, int d2,int e) {
    if (B[index_B(a,d, d2,e)] > INT_MIN) {
        return B[index_B(a,d, d2,e)];
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (d-1!=d2) && (d-1!=e);
    bool eq_some_const2 = (d-1!=d2) && (d-1!=e);

    if (a+1 < d) {
        if (!eq_some_const1) {
            min_value = min(min_value, compute_B(a+1,d,d2,e));
        }
    }
    if (d-1 > a) {
        if (!eq_some_const2) {
            min_value = min(min_value, compute_B2(a, d-1, d2,e));
        }
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_B(a+1, d-1, d2,e)+bp_score(line[a], 
                                                                                      line[d]));
    }

    min_value = min(min_value, compute_CLIQUE(1,13,d2,e));

    B[index_B(a,d,d2,e)] = min_value;
    return min_value;
} 

int compute_B2(int a, int d, int d2,int e) {
    if (B2[index_B(a,d, d2,e)] > INT_MIN) {
        return B2[index_B(a,d, d2,e)];
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (d-1!=d2) && (d-1!=e);
    bool eq_some_const2 = (d-1!=d2) && (d-1!=e);

    if (d-1 > a && !eq_some_const2) {
        min_value = min(min_value, compute_B2(a, d-1, d2,e));
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_B(a+1, d-1, d2,e)+bp_score(line[a], 
                                                                                      line[d]));
    }

    B2[index_B(a,d,d2,e)] = min_value;
    return min_value;
}


