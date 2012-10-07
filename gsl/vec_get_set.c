#include <stdio.h>
#include <gsl/gsl_vector.h>

static double v2;

int main(int argc, char * argv[]) {

    gsl_vector * v = gsl_vector_calloc(3);

    v2 = gsl_vector_get(v, 2);
    printf("%f\n", v2);

    gsl_vector_set(v, 2, 84.0);

    v2 = gsl_vector_get(v, 2);
    printf("%f\n", v2);

    gsl_vector_free(v);

    return 0;
}
