/* 
 * Numerical integration of some functions using the rectangle method (top-left
 * corner approximation).
 */

#include <stdio.h>
#include <stdlib.h>

#include "numerical_integration.h"
#include "test_func.h"

/*
 * Main function.
 */
int main(int argc, char * argv[])
{
    double min=-5.0;
    double max=5.0;

    /* function 1 */
    fprintf(stdout, "Numerical integration: %f\n", integrate_using_rectangle_rule(f1, min, max));
    fprintf(stdout, "Exact value: %f\n", F1(max) - F1(min));

    /* function 2 */
    fprintf(stdout, "\nNumerical integration: %f\n", integrate_using_rectangle_rule(f2, min, max));
    fprintf(stdout, "Exact value: %f\n", F2(max) - F2(min));
    
    return EXIT_SUCCESS;
}
