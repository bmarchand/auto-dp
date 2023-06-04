#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>

int min(int a, int b) { if (a<b) {return a;} else {return b;}};

int index_B(int a,int e,int f,int j);
int index_C(int a,int d,int f,int i);
int index_D(int b,int d,int g,int i);
int index_CLIQUE(int i, int j, int k, int l);

void init_fill_B();
void init_fill_C();
void init_fill_D();
void init_fill_CLIQUE();

int compute_A();
int compute_B(int a,int e,int f,int j);
int compute_C(int a,int d,int f,int i);
int compute_D(int b,int d,int g,int i);
int fold();

int n;

char * line = NULL;

double * B;
double * C;
double * D;
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
    double * C = malloc(n*n*n*n*sizeof(double));
    double * D = malloc(n*n*n*n*sizeof(double));
    double * CLIQUE = malloc(n*n*n*n*sizeof(double));
    init_fill_B();
    init_fill_C();
    init_fill_D();
    init_fill_CLIQUE();
    int score = fold();
    char * structure = NULL;
    structure = backtrace();
    free(B);
    free(C);
    free(D);
    free(CLIQUE);
}
int bp_score(char x, char y) {
    if (x=='G' && y=='C') { return 10; }
    if (x=='C' && y=='G') { return 10; }
    if (x=='G' && y=='U') { return 5; }
    if (x=='U' && y=='G') { return 5; }
    if (x=='A' && y=='U') { return 5; }
    if (x=='U' && y=='A') { return 5; }
    return 0;
}
int fold() {
    compute_A();
    }

int compute_CLIQUE2(int i, int j, int k, int l);

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
        for (int e=a;e<n;e++) {
            for (int f=e;f<n;f++) {
                for (int j=f;j<n;j++) {
                    B[index_B(a,e,f,j)] = INT_MIN;
                }
            }
        }
    }
}

int index_B(int a,int e,int f,int j)  {
    return n*n*n*a+n*n*e+n*f+j;
}

void init_fill_C() {
    for (int a=0;a<n;a++) {
        for (int d=a;d<n;d++) {
            for (int f=d;f<n;f++) {
                for (int i=f;i<n;i++) {
                    C[index_C(a,d,f,i)] = INT_MIN;
                }
            }
        }
    }
}

int index_C(int a,int d,int f,int i)  {
    return n*n*n*a+n*n*d+n*f+i;
}

void init_fill_D() {
    for (int b=0;b<n;b++) {
        for (int d=b;d<n;d++) {
            for (int g=d;g<n;g++) {
                for (int i=g;i<n;i++) {
                    D[index_D(b,d,g,i)] = INT_MIN;
                }
            }
        }
    }
}

int index_D(int b,int d,int g,int i)  {
    return n*n*n*b+n*n*d+n*g+i;
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
        for (int e=a;e<n;e++) {
            for (int f=e;f<n;f++) {
                for (int j=f;j<n;j++) {
                    for (int k=j;k<n;k++) {
                        min_value = min(min_value, compute_B(j,a,e,f)+compute_CLIQUE(e,f,j,k));
                    }
                }
            }
        }
    }

    return min_value;
}

int compute_B(int a,int e,int f,int j) {
    if (B[index_B(a,e,f,j)] > INT_MIN) {
        return B[index_B(a,e,f,j)];
    }
    
    int min_value = INT_MAX;
    
    for (int d=a;d<j;d++) {
        for (int i=d;i<j;i++) {
            min_value = min(min_value, compute_C(f,a,d,i)+compute_CLIQUE(d,e,i,j));
        }
    }

    B[index_B(a,e,f,j)] = min_value;
    return min_value;
}

int compute_C(int a,int d,int f,int i) {
    if (C[index_C(a,d,f,i)] > INT_MIN) {
        return C[index_C(a,d,f,i)];
    }
    
    int min_value = INT_MAX;
    
    for (int g=f;g<i;g++) {
        for (int b=g;b<n;b++) {
            min_value = min(min_value, compute_CLIQUE(a,b,f,g)+compute_D(g,b,d,i));
        }
    }

    C[index_C(a,d,f,i)] = min_value;
    return min_value;
}


int compute_D(int b,int d,int g,int i) {
    if (D[index_D(b,d,g,i)] > INT_MIN) {
        return D[index_D(b,d,g,i)];
    }
    
    int min_value = INT_MAX;
    
    for (int h=g;h<i;h++) {
        for (int c=h;c<n;c++) {
            min_value = min(min_value, compute_CLIQUE(b,c,g,h)+compute_CLIQUE(c,d,h,i));
        }
    }

    D[index_D(b,d,g,i)] = min_value;
    return min_value;
}




