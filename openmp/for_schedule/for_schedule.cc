/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c for_schedule.cc
 *    g++ -fopenmp for_schedule.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./for_schedule
 * will use 2 cores.
 */

#include <iostream>
#include <omp.h>

static const int N = 16;

int main()
{
    std::cout << "#pragma omp parallel for" << std::endl;

    #pragma omp parallel for
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": " << i << std::endl;
        }
    }

    std::cout << "#pragma omp parallel for schedule(static, 1)" << std::endl;
    
    #pragma omp parallel for schedule(static, 1)
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": " << i << std::endl;
        }
    }

    std::cout << "#pragma omp parallel for schedule(dynamic, 1)" << std::endl;
    
    #pragma omp parallel for schedule(dynamic, 1)
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": " << i << std::endl;
        }
    }

    std::cout << "#pragma omp parallel for schedule(dynamic, 2)" << std::endl;
    
    #pragma omp parallel for schedule(dynamic, 2)
    for(int i = 0; i < N; i++)
    {
        int th_id = omp_get_thread_num();

        #pragma omp critical
        {
            std::cout << "thread " << th_id << ": " << i << std::endl;
        }
    }

    return 0;
}
