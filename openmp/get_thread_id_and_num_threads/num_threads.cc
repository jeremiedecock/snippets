/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c num_threads.cc
 *    g++ -fopenmp num_threads.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./num_threads
 * will use 2 cores.
 */

#include <iostream>
#include <omp.h>

int main(int argc, char *argv[])
{
    int th_id, nthreads;
    #pragma omp parallel private(th_id) shared(nthreads)
    {
        th_id = omp_get_thread_num();
        #pragma omp critical
        {
            std::cout << "Hello World from thread " << th_id << std::endl;
        }
        #pragma omp barrier

        #pragma omp master
        {
            nthreads = omp_get_num_threads();
            std::cout << "There are " << nthreads << " threads" << std::endl;
        }
    }

    return 0;
}
