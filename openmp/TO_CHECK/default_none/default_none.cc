#include <iostream>
#include <omp.h>

int main(int argc, char *argv[])
{
    int a=0, b=0, c=0, d=0, f=0, g=0, i, id;

    #pragma omp parallel default(none)
    {
        int z=0;

        id = omp_get_thread_num();

        for(i=0 ; i<10 ; i++) {
            a++;
            b++;
            c++;
            d++;
        #pragma omp atomic
            f++;
        #pragma omp barrier
        #pragma omp critical
            g++;
        #pragma omp barrier
            z++;
        }

        #pragma omp critical
        {
            std::cout << "thread " << id << ": ";
            std::cout << "a=" << a << " ";
            std::cout << "b=" << b << " ";
            std::cout << "c=" << c << " ";
            std::cout << "d=" << d << " ";
            std::cout << "f=" << f << " ";
            std::cout << "g=" << g << " ";
            std::cout << "z=" << z << " ";
            std::cout << "i=" << i;
            std::cout << std::endl;
        }
        #pragma omp barrier
    }

    std::cout << "master:   ";
    std::cout << "a=" << a << " ";
    std::cout << "b=" << b << " ";
    std::cout << "c=" << c << " ";
    std::cout << "d=" << d << " ";
    std::cout << "f=" << f << " ";
    std::cout << "g=" << g << " ";
    std::cout << std::endl;

    return 0;
}
