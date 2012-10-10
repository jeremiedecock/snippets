/* 
 * Gsl_blas_dgemv: test gsl_blas_dgemv (matrix . vector)
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: GSL library (libgsl0-dev)
 * Usage: gcc gsl_blas_dgemv.c -lgsl -lgslcblas -lm
 *    or: gcc gsl_blas_dgemv.c $(pkg-config --libs gsl)
 */

#include <gsl/gsl_blas.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>

void main() {

    gsl_vector * v = gsl_vector_alloc(3);
    gsl_vector * r = gsl_vector_alloc(3);
    gsl_matrix * m = gsl_matrix_alloc(3, 3);

    gsl_vector_set_all(v, 2.0);
    gsl_matrix_set_all(m, 3.0);

    gsl_blas_dgemv(CblasNoTrans,
                   1.0, m, v,
                   0.0, r);

    gsl_vector_fprintf(stdout, r, "%f");

    gsl_vector_free(v);
    gsl_vector_free(r);
    gsl_matrix_free(m);

}
