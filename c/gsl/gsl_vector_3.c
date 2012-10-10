/* 
 * Gsl_vector_3: test gsl_vector
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: GSL library (libgsl0-dev)
 * Usage: gcc gsl_vector_3.c -lgsl -lgslcblas -lm
 *    or: gcc gsl_vector_3.c $(pkg-config --libs gsl)
 */

#include <gsl/gsl_vector.h>

int main(int argc, char * argv[]) {

    gsl_vector * v1 = gsl_vector_calloc(10);
    gsl_vector * v2 = gsl_vector_calloc(10);

    gsl_vector_set_all(v1, 2.0);
    gsl_vector_set_all(v2, 6.0);

    gsl_vector_mul(v1, v2);

    gsl_vector_fprintf(stdout, v1, "%.2f");

    gsl_vector_free(v1);
    gsl_vector_free(v2);

    return 0;
}
