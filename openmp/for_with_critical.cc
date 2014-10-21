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
