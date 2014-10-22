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
