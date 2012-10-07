#include <stdio.h>
#include <gsl/gsl_matrix.h>

#define I 3
#define J 3

int main(int argc, char * argv[]) {

    gsl_matrix * m = gsl_matrix_alloc(I, J);

    gsl_matrix_set_identity(m);

    //gsl_matrix_fprintf(stdout, m, "%f");

    int i, j;
    for(i=0 ; i<I ; i++) {
        for(j=0 ; j<J ; j++) {
            printf("%2.1f ", gsl_matrix_get(m, i, j));
        }
        printf("\n");
    }

    gsl_matrix_free(m);

    return 0;
}

