/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c rand.cc
 *    g++ -fopenmp rand.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./rand
 * will use 2 cores.
 */

#include <iostream>
#include <cstdlib>

static const int N = 20;              // Number of integrate to compute
static const int CHUNKSIZE = 1;       // Defines the chunk size as 1 contiguous iteration

//////////////////////////////////////////

void print_tab(const int (& t)[N])
{
    for(int i=0 ; i<N ; i++) {
        std::cout << t[i] << std::endl;
    }
}

//////////////////////////////////////////

int main()
{
    int t[N];

    srand(1);

    // Forks off the threads
    #pragma omp parallel
    {
        // Starts the work sharing construct (static / dynamic)
        #pragma omp for schedule(dynamic, CHUNKSIZE)
        for(int i = 0 ; i < N ; i++)
            t[i] = rand();
    }

    print_tab(t);

    return 0;
}
