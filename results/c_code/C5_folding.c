#include <stdio.h>
#include <limits.h>
#include <stdlib.h>

int min(int a, int b) { if (a<b) {return a;} else {return b;}};

int index_B(int n,int a,int g,int h,int j);
int index_C(int n,int a,int e,int f,int g,int i,int j);
int index_D(int n,int d,int f,int g,int i,int j,int b);
int index_CLIQUE(int i, int j, int k, int l);

void init_fill_B();
void init_fill_C();
void init_fill_D();
void init_fill_CLIQUE();

int n;

double * B;
double * C;
double * D;
double * CLIQUE;
double * CLIQUE2;

int compute_A();
int fold(char* line);

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
    double * D = malloc(n*n*n*n*n*n*sizeof(double));
    double * CLIQUE = malloc(n*n*n*n*sizeof(double));
    init_fill_B();
    init_fill_C();
    init_fill_D();
    init_fill_CLIQUE();
    int score = fold(line);
    free(B);
    free(C);
    free(D);
    free(CLIQUE);
}
int fold(char* line) {
    compute_A();
    }

int compute_CLIQUE2(int i, int j, int k, int l, char * line);

int bp_score(char x, char y) {
    if (x=='G' && y=='C') { return 10; }
    if (x=='C' && y=='G') { return 10; }
    if (x=='G' && y=='U') { return 5; }
    if (x=='U' && y=='G') { return 5; }
    if (x=='A' && y=='U') { return 5; }
    if (x=='U' && y=='A') { return 5; }
    return 0;
}

int compute_CLIQUE(int i, int j, int k, int l, char * line) {
    //C_boxtimes in article"
    if (CLIQUE[index_CLIQUE(i,j,k,l)] > INT_MIN) { 
        return CLIQUE[index_CLIQUE(i,j,k,l)];
    }
    
    int min_value = INT_MAX;

    if (k < l) { 
        min_value = min(min_value, compute_CLIQUE2(i,j,k,l-1,line)); 
    }
    if (i < j) {
        min_value = min(min_value, compute_CLIQUE(i+1,j,k,l,line));
    }
    if (i < j && k < l) {
        min_value = min(min_value, 
                    compute_CLIQUE(i+1, j, k, l-1,line)+bp_score(line[i],line[l]));
    }
    if (k==l) { 
        min_value = min(min_value, bp_score(line[i], line[l]));
    }

    CLIQUE[index_CLIQUE(i,j,k,l)] = min_value;
    return min_value;
}

int compute_CLIQUE2(int i, int j, int k, int l, char * line) {
    //C_boxtimes' in article:w

    if (CLIQUE2[index_CLIQUE(i,j,k,l)] > INT_MIN) { 
        return CLIQUE2[index_CLIQUE(i,j,k,l)];
    }
    int min_value = INT_MAX;

    if (k < l) { 
        min_value = min(min_value, compute_CLIQUE2(i,j,k,l-1,line)); 
    }
    if (i < j && k < l) {
        min_value = min(min_value, 
                    compute_CLIQUE(i+1, j, k, l-1, line)+bp_score(line[i],line[l]));
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
                    B[index_B(n,a,g,h,j)] = INT_MIN;
                }
            }
        }
    }
}

int index_B(int n,int a,int g,int h,int j)  {
    return n*n*n*a+n*n*g+n*h+j;
}

void init_fill_C() {
    for (int a=0;a<n;a++) {
        for (int e=a;e<n;e++) {
            for (int f=e;f<n;f++) {
                for (int g=f;g<n;g++) {
                    for (int i=g;i<n;i++) {
                        for (int j=i;j<n;j++) {
                            C[index_C(n,a,e,f,g,i,j)] = INT_MIN;
                        }
                    }
                }
            }
        }
    }
}

int index_C(int n,int a,int e,int f,int g,int i,int j)  {
    return n*n*n*n*n*a+n*n*n*n*e+n*n*n*f+n*n*g+n*i+j;
}

void init_fill_D() {
    for (int d=0;d<n;d++) {
        for (int f=d;f<n;f++) {
            for (int g=f;g<n;g++) {
                for (int i=g;i<n;i++) {
                    for (int j=i;j<n;j++) {
                        for (int b=j;b<n;b++) {
                            D[index_D(n,d,f,g,i,j,b)] = INT_MIN;
                        }
                    }
                }
            }
        }
    }
}

int index_D(int n,int d,int f,int g,int i,int j,int b)  {
    return n*n*n*n*n*d+n*n*n*n*f+n*n*n*g+n*n*i+n*j+b;
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
    
    for (int a=0;a<k;a++) {
        for (int g=a;g<k;g++) {
            for (int h=g;h<k;h++) {
                for (int j=h;j<k;j++) {
                    for (int k=j;k<n;k++) {
                        min_value = min(min_value, compute_B(j,a,g,h)+compute_CLIQUE(g,h,j,k));
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
    
    for (int e=a;e<i;e++) {
        for (int f=e;f<i;f++) {
            for (int i=f;i<j;i++) {
                min_value = min(min_value, compute_C(a,e,f,g,i,j)+compute_CLIQUE(e,f,h,i));
            }
        }
    }

    B[index_B(a,g,h,j)] = min_value;
    return min_value;
}

int compute_C(int e, int a, int f,int j,int i,int g, line) {
    if (C[index_C(e,a, f,j,i,g)] > INT_MIN) {
        return C[index_C(e,a, f,j,i,g)];
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (a-1!=f) || (a-1!=j) || (a-1!=i) || (a-1!=g);
    bool eq_some_const2 = (a-1!=f) || (a-1!=j) || (a-1!=i) || (a-1!=g);

    if (e+1 < a) {
        if (!eq_some_const1) {
            min_value = min(min_value, compute_C(e+1,a,f,j,i,g));
        }
    }
    if (a-1 > e) {
        if (!eq_some_const2) {
            min_value = min(min_value, compute_C2(e, a-1, f,j,i,g));
        }
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_C(e+1, a-1, f,j,i,g)+bp_score(line[e], 
                                                                                      line[a]));
    }

    min_value = min(min_value, compute_D(f,j,i,17,1,g));

    C[index_C(e,a,f,j,i,g)] = min_value;
    return min_value;
} 

int compute_C2(int e, int a, int f,int j,int i,int g, line) {
    if (C2[index_C(e,a, f,j,i,g)] > INT_MIN) {
        return C2[index_C(e,a, f,j,i,g)]
    }

    int min_value = INT_MAX;
    bool eq_some_const1 = (a-1!=f) || (a-1!=j) || (a-1!=i) || (a-1!=g);
    bool eq_some_const2 = (a-1!=f) || (a-1!=j) || (a-1!=i) || (a-1!=g);

    if (a-1 > e && !eq_some_const2) {
        min_value = min(min_value, compute_C2(e, a-1, f,j,i,g);
    }
    if (!eq_some_const1 && !eq_some_const2) {
        min_value = min(min_value, compute_C(e+1, a-1, f,j,i,g)+bp_score(line[e], 
                                                                                      line[a]));
    }

    C2[index_C2(e,a,f,j,i,g)] = min_value;
    return min_value;
}


int compute_D(int d,int f,int g,int i,int j,int b) {
    if (D[index_D(d,f,g,i,j,b)] > INT_MIN) {
        return D[index_D(d,f,g,i,j,b)];
    }
    
    int min_value = INT_MAX;
    
    for (int c=b;c<n;c++) {
        min_value = min(min_value, compute_CLIQUE(c,d,f,g)+compute_CLIQUE(b,c,i,j));
    }

    D[index_D(d,f,g,i,j,b)] = min_value;
    return min_value;
}




