#include "numerical_integration.h"

/* Size of subintervals (base of rectangles) */
static double delta = 0.0000001;

/*
 * Numerical integration of (*pf) between min and max using the rectangle
 * method (top-left corner approximation).
 */
double integrate_using_rectangle_rule(double (*pf)(double), double min, double max) {
    double sum = 0.0;

    double i;
    for(i=min ; i<=max ; i+=delta) {
        double y = (*pf)(i);
        double rectangle_area = y * delta;
        sum += rectangle_area;
    }

    return sum;
}
