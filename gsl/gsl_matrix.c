/* 
 * Gsl_matrix: test gsl_matrix
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: GSL library (libgsl0-dev)
 * Usage: gcc gsl_matrix.c -lgsl -lgslcblas -lm
 *    or: gcc gsl_matrix.c $(pkg-config --libs gsl)
 */

#include <gsl/gsl_matrix.h>

#define N 10

int main(int argc, char * argv[]) {

    gsl_matrix * m1 = gsl_matrix_calloc(N, N);
    gsl_matrix * m2 = gsl_matrix_calloc(N, N);

    gsl_matrix_set_all(m1, 2.0);
    gsl_matrix_set_all(m2, 6.0);

    gsl_matrix_mul_elements(m1, m2);

    gsl_matrix_fprintf(stdout, m1, "%.2f");

    gsl_matrix_free(m1);
    gsl_matrix_free(m2);

    return 0;

}
