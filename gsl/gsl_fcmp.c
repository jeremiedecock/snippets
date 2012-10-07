#include <gsl/gsl_sys.h>
#include <stdio.h>

void main(void) {

    double n1, n2, eps;

    n1 = 1.0;
    n2 = 1.1;

    eps = 0.2;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    eps = 0.1;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));
    
    eps = 0.05;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 0.01;
    n2 = 0.0;
    eps = 0.1;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 0.01;
    n2 = 0.000001;
    eps = 0.1;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 1.01;
    n2 = 1.000001;
    eps = 0.1;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 0.51;
    n2 = 0.500001;
    eps = 0.1;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 0.51;
    n2 = 0.500001;
    eps = 0.01;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

    n1 = 0.51;
    n2 = 0.5;
    eps = 0.02;

    printf("%f ~ %f (+/- %f) : %d\n", n1, n2, eps, gsl_fcmp(n1, n2, eps));

}
