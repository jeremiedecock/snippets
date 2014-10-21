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
