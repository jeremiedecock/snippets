#include <sys/time.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main(void) {

    struct timeval timev;

    gettimeofday(&timev, NULL);

    fprintf(stdout, "%ld\n", time(NULL));
    fprintf(stdout, "%ld.%06ld\n", timev.tv_sec, timev.tv_usec);

    exit(EXIT_SUCCESS);

}
