#include <sys/time.h>
#include <stdio.h>

void main(void) {

    struct timeval timev_start, timev_end, timev_diff;

    gettimeofday(&timev_start, NULL);

    fprintf(stdout, "hello\n");
    fprintf(stdout, "hello\n");

    gettimeofday(&timev_end, NULL);

    timersub(&timev_end, &timev_start, &timev_diff);

    fprintf(stdout, "%ld.%06ld\n", timev_diff.tv_sec, timev_diff.tv_usec);

}
