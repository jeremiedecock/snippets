#include "test_func.h"
#include <math.h>

/*
 * Function 1: x²
 */
double f1(double x) {
    double y = pow(x, 2);
    return y;
}

/*
 * Antiderivative function of x² (to check the numerical integration accuracy)
 */
double F1(double x) {
    double Y = (1.0/3.0) * pow(x, 3);
    return Y;
}


/*
 * Function 2: x²-2
 */
double f2(double x) {
    double y = pow(x, 2) - 2.0;
    return y;
}

/*
 * Antiderivative function of x²-2 (to check the numerical integration accuracy)
 */
double F2(double x) {
    double Y = (1.0/3.0) * pow(x, 3) - 2.0 * x;
    return Y;
}
