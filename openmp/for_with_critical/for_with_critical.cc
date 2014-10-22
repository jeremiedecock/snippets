/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c for_with_critical.cc
 *    g++ -fopenmp for_with_critical.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./for_with_critical
 * will use 2 cores.
 */

#include <iostream>
#include <omp.h>

static const int N = 12;

int main()
{
    std::cout << "#pragma omp parallel for" << std::endl;

    #pragma omp parallel for
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": ";
            std::cout << i << std::endl;
        }

        int j = i * -1;

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": ";
            std::cout << j << std::endl;
        }
    }

    return 0;
}
