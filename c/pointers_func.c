/* 
 * Copyright (c) 2013 Jérémie Decock
 *
 * Usage: gcc pointers_func.c
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define DELTA 0.00001

////////

double f1(double x) {
    return  pow(x, 2.);
}

// TAKE A FUNCTION //////

double integ(double (*pf)(double), double a, double b)
{
    double x, sum;

    for(x=a ; x<=b ; x+=DELTA) {
        sum += pf(x) * DELTA;
    }

    return sum;
}

// RETURN A FUNCTION //////

double (* factory(void)) (double)
{
    return f1;
}

////////

int main(int argc, char * argv[])
{
    double (*pf)(double);
    pf = f1;

    double y1, y2;
    y1 = (*pf)(3.);
    y2 = pf(3.);

    printf("%f\n", y1);
    printf("%f\n", y2);

    ////
    
    printf("integ(x^2, 0., 1.) = %f\n", integ(f1, 0., 1.));
    
    ////

    pf = factory();
    printf("%f\n", pf(3.));

    exit(EXIT_SUCCESS);
}

