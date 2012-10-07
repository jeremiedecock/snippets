#include <stdio.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_matrix.h>

int main (void)
{
    gsl_matrix * m1 = gsl_matrix_alloc(3, 3);
    gsl_matrix * m2 = gsl_matrix_alloc(3, 3);
    gsl_matrix * m3 = gsl_matrix_alloc(3, 3);

    gsl_matrix_set_all(m1, 3.0);
    gsl_matrix_set_all(m2, 2.0);

    /* Compute m3 = m1.m2 */

    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans,
                   1.0, m1, m2,
                   0.0, m3);

    int i, j;
    for(i=0 ; i<3 ; i++) {
        printf("[");
        for(j=0 ; j<3 ; j++) {
            printf(" %f ", gsl_matrix_get(m3, i, j));
        }
        printf("]\n");
    }

    gsl_matrix_free(m1);
    gsl_matrix_free(m2);
    gsl_matrix_free(m3);

    return 0;  
}

