/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c clause_scope.cc
 *    g++ -fopenmp clause_scope.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./clause_scope
 * will use 2 cores.
 */

#include <iostream>
#include <omp.h>

static const int N = 8;

int main()
{
    std::cout << "OK:" << std::endl;

    #pragma omp parallel for
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": " << i << std::endl;
            std::cout << "------" << std::endl;
        }
    }

    std::cout << std::endl << "NOT OK:" << std::endl;

    #pragma omp parallel for
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        std::cout << "thread " << th_id << ": " << i << std::endl;
        std::cout << "------" << std::endl;
    }

    return 0;
}
