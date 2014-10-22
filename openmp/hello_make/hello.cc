/*
 * A very basic demo of OpenMP.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c hello.cc
 *    g++ -fopenmp hello.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./hello
 * will use 2 cores.
 */

#include <iostream>

int main() {
#pragma omp parallel
    std::cout << "Hello world" << std::endl;
    return 0;
}
