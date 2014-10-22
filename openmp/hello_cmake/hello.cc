/* 
 * A very basic demo of OpenMP.
 *
 * USAGE:
 *    g++ -fopenmp -c hello.cc
 *    g++ -fopenmp hello.o
 */

#include <iostream>

int main() {
#pragma omp parallel
    std::cout << "Hello world" << std::endl;
    return 0;
}
