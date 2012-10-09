/* 
 * Gsl_vector: test gsl_vector
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: GSL library (libgsl0-dev)
 * Usage: gcc gsl_vector.c -lgsl -lgslcblas -lm
 *    or: gcc gsl_vector.c $(pkg-config --libs gsl)
 */

#include <stdio.h>
#include <gsl/gsl_vector.h>

static double v2;

int main(int argc, char * argv[]) {

    gsl_vector * v = gsl_vector_calloc(3);

    gsl_vector_set_all(v, 84.0);

    gsl_vector_fprintf(stdout, v, "%f");

    gsl_vector_free(v);

    return 0;
}

