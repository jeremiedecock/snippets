/* 
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc pi.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

const unsigned long num_random_points = 1000000;

/*
 * Main
 */
int main(int argc, char * argv[])
{
    unsigned long inside_circle = 0;

    srand(getpid());

    unsigned long i;
    for(i=0 ; i<num_random_points ; i++) {
        double x = (double) rand() / (double) RAND_MAX;
        double y = (double) rand() / (double) RAND_MAX;

        if((x*x + y*y) <= 1.0) {
            inside_circle++;
        }
    }

    double pi = (double) inside_circle / (double) num_random_points * 4.0;
    printf("pi=%f\n", pi);

    return 0;
}
