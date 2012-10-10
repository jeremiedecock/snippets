/* 
 * Gsl_blas_ddot: test gsl_blas_ddot (vector . vector)
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: GSL library (libgsl0-dev)
 * Usage: gcc gsl_blas_ddot.c -lgsl -lgslcblas -lm
 *    or: gcc gsl_blas_ddot.c $(pkg-config --libs gsl)
 */

#include <stdio.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_vector.h>

int main (void)
{
    gsl_vector * v1 = gsl_vector_alloc(3);
    gsl_vector * v2 = gsl_vector_alloc(3);

    gsl_vector_set_all(v1, 3.0);
    gsl_vector_set_all(v2, 2.0);

    double r;
    gsl_blas_ddot(v1, v2, &r);

    printf("%f\n", r);

    gsl_vector_free(v1);
    gsl_vector_free(v2);

    return 0;  
}

