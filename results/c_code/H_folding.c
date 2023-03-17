#include <stdio.h>
#include <stdlib.h>
int main(int argc, char ** argv) {
    char * line = NULL;
    size_t len = 0;
    FILE * fp = fopen(argv[1], "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);
    while( getline(&line, &len, fp)!=-1) {
        printf("%s", line);
    }
}
