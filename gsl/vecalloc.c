#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <time.h>

#define N 50

int main(int argc, char * argv[]) {
    
    clock_t t1 = clock();

    //gsl_vector * v1 = gsl_vector_calloc(1000);
    //gsl_vector * v2 = gsl_vector_calloc(1000);

    gsl_matrix * m1 = gsl_matrix_calloc(N, N);
    gsl_matrix * m2 = gsl_matrix_calloc(N, N);

    //gsl_vector_set_all(v1, 2.0);
    //gsl_vector_set_all(v2, 6.0);

    gsl_matrix_set_all(m1, 2.0);
    gsl_matrix_set_all(m2, 6.0);

    //gsl_vector_mul(v1, v2);
    gsl_matrix_mul_elements(m1, m2);

    //gsl_vector_fprintf(stdout, v1, "%.2f");
    gsl_matrix_fprintf(stdout, m1, "%.2f");

    //gsl_vector_free(v1);
    //gsl_vector_free(v2);

    gsl_matrix_free(m1);
    gsl_matrix_free(m2);
    
    clock_t t2 = clock();
    clock_t et = t2 - t1;

    printf("%u\n", t1);
    printf("%u\n", t2);
    printf("%u\n", et);
    printf("%f\n", (double) et / (double) CLOCKS_PER_SEC);

    return 0;
}
