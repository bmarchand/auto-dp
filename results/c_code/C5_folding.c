#include <stdio.h>
#include <limits.h>
#include <stdlib.h>
#include <stdbool.h>

int min(int a, int b) { if (a<b) {return a;} else {return b;}};

int index_B(int a,int g,int h,int j);
int index_C(int a,int e,int f,int g,int i,int j);
int index_D(int b,int d,int f,int g,int i,int j);
int index_CLIQUE(int i, int j, int k, int l);

void init_fill_B();
void init_fill_C();
void init_fill_D();
void init_fill_CLIQUE();

int compute_A();
int compute_B(int a,int g,int h,int j);
int compute_C(int a,int e,int f,int g,int i,int j);
int compute_C2(int a,int e,int f,int g,int i,int j);
int compute_D(int b,int d,int f,int g,int i,int j);
int fold();

int n;

char * line = NULL;

double * B;
double * C;
double * C2;
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
    double * C = malloc(n*n*n*n*n*n*sizeof(double));
double * C2 = malloc(n*n*n*n*n*n*sizeof(double));
    double * D = malloc(n*n*n*n*n*n*sizeof(double));
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
        for (int g=a;g<n;g++) {
            for (int h=g;h<n;h++) {
                for (int j=h;j<n;j++) {
                    B[index_B(a,g,h,j)] = INT_MIN;
                }
            }
        }
    }
}

int index_B(int a,int g,int h,int j)  {
    return n*n*n*a+n*n*g+n*h+j;
}

void init_fill_C() {
    for (int a=0;a<n;a++) {
        for (int e=a;e<n;e++) {
            for (int f=e;f<n;f++) {
                for (int g=f;g<n;g++) {
                    for (int i=g;i<n;i++) {
                        for (int j=i;j<n;j++) {
                            C[index_C(a,e,f,g,i,j)] = INT_MIN;
                        }
                    }
                }
            }
        }
    }
}

int index_C(int a,int e,int f,int g,int i,int j)  {
    return n*n*n*n*n*a+n*n*n*n*e+n*n*n*f+n*n*g+n*i+j;
}

void init_fill_D() {
    for (int b=0;b<n;b++) {
        for (int d=b;d<n;d++) {
            for (int f=d;f<n;f++) {
                for (int g=f;g<n;g++) {
                    for (int i=g;i<n;i++) {
                        for (int j=i;j<n;j++) {
                            D[index_D(b,d,f,g,i,j)] = INT_MIN;
                        }
                    }
                }
            }
        }
    }
}

int index_D(int b,int d,int f,int g,int i,int j)  {
    return n*n*n*n*n*b+n*n*n*n*d+n*n*n*f+n*n*g+n*i+j;
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
        for (int g=a;g<n;g++) {
            for (int h=g;h<n;h++) {
                for (int j=h;j<n;j++) {
                    for (int k=j;k<n;k++) {
                        min_value = min(min_value, compute_B(h,j,a,g)+compute_CLIQUE(g,h,j,k));
                    }
                }
            }
        }
    }

    return min_value;
}

int compute_B(int a,int g,int h,int j) {
    if (B[index_B(a,g,h,j)] > INT_MIN) {
        return B[index_B(a,g,h,j)];
    }
    
    int min_value = INT_MAX;
    
    for (int e=a;e<j;e++) {
        for (int f=e;f<j;f++) {
            for (int i=f;i<j;i++) {
                min_value = min(min_value, compute_C(a,e,f,g,i,j)+compute_CLIQUE(e,f,h,i));
            }
        }
    }

    B[index_B(a,g,h,j)] = min_value;
    return min_value;
}

int compute_C(int a, int e, int j,int i,int f,int g) {
    if (C[index_C(a,e, j,i,f,g)] > INT_MIN) {
        return C[index_C(a,e, j,i,f,g)];
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (e-1!=j) && (e-1!=i) && (e-1!=f) && (e-1!=g);
    bool eq_some_const2 = (e-1!=j) && (e-1!=i) && (e-1!=f) && (e-1!=g);

    if (a+1 < e) {
        if (!eq_some_const1) {
            min_value = min(min_value, compute_C(a+1,e,j,i,f,g));
        }
    }
    if (e-1 > a) {
        if (!eq_some_const2) {
            min_value = min(min_value, compute_C2(a, e-1, j,i,f,g));
        }
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_C(a+1, e-1, j,i,f,g)+bp_score(line[a], 
                                                                                      line[e]));
    }

    min_value = min(min_value, compute_D(g,17,i,1,j,f));

    C[index_C(a,e,j,i,f,g)] = min_value;
    return min_value;
} 

int compute_C2(int a, int e, int j,int i,int f,int g) {
    if (C2[index_C(a,e, j,i,f,g)] > INT_MIN) {
        return C2[index_C(a,e, j,i,f,g)];
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (e-1!=j) && (e-1!=i) && (e-1!=f) && (e-1!=g);
    bool eq_some_const2 = (e-1!=j) && (e-1!=i) && (e-1!=f) && (e-1!=g);

    if (e-1 > a && !eq_some_const2) {
        min_value = min(min_value, compute_C2(a, e-1, j,i,f,g));
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_C(a+1, e-1, j,i,f,g)+bp_score(line[a], 
                                                                                      line[e]));
    }

    C2[index_C(a,e,j,i,f,g)] = min_value;
    return min_value;
}


int compute_D(int b,int d,int f,int g,int i,int j) {
    if (D[index_D(b,d,f,g,i,j)] > INT_MIN) {
        return D[index_D(b,d,f,g,i,j)];
    }
    
    int min_value = INT_MAX;
    
    for (int c=j;c<n;c++) {
        min_value = min(min_value, compute_CLIQUE(c,d,f,g)+compute_CLIQUE(b,c,i,j));
    }

    D[index_D(b,d,f,g,i,j)] = min_value;
    return min_value;
}




