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
