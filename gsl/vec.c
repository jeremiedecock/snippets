#include <stdlib.h>
#include <stdio.h>
#include <gsl/gsl_vector.h>

int main(int argc, char * argv[]) {
    
    gsl_vector * vec = gsl_vector_calloc(3);

    gsl_vector_set(vec, 0, 10.0);
    gsl_vector_set(vec, 1, 20.0);
    gsl_vector_set(vec, 2, 30.0);

    int i = 0;
    for(i=0 ; i<3 ; i++)
        fprintf(stdout, "%f\n", gsl_vector_get (vec, i));

    gsl_vector_fprintf(stdout, vec, "%f");

    gsl_vector_free(vec);

    exit(EXIT_SUCCESS);
}
