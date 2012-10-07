#include <stdio.h>

void main() {

    FILE * fd = fopen("test.txt", "r");

    if(NULL != fd) {

        char str;

        while(1) {
            fscanf(fd, "%c", &str);
            if(feof(fd)) break;
            fprintf(stdout, "%c", str);
        }

        fclose(fd);

    }

}

