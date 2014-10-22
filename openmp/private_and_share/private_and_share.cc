/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c private_and_share.cc
 *    g++ -fopenmp private_and_share.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./private_and_share
 * will use 2 cores.
 */

#include <iostream>
#include <omp.h>

int main(int argc, char *argv[])
{
    int a=0, b=0, c=0, d=0, f=0, g=0, i, id;

    #pragma omp parallel shared(b) private(c, i, id) firstprivate(d)
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
