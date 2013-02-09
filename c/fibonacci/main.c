#include <stdio.h>
#include "fibonacci.h"

int main(void)
{
    long n = fibonacci(10);
    printf("fibonacci(10)=%ld\n", n);

    return 0;
}
