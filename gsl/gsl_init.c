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

