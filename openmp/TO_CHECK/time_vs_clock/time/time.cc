/*
 * An OpenMP snippet.
 *
 * USAGE (GCC):
 *    g++ -fopenmp -c time.cc
 *    g++ -fopenmp time.o
 *
 * In order to use N cores, the shell environment variable OMP_NUM_THREADS
 * should be set (at execution time not at compilation time):
 *    export OMP_NUM_THREADS=N
 *
 * For instance,
 *    export OMP_NUM_THREADS=2
 *    ./time
 * will use 2 cores.
 */

#include <iostream>
#include <cmath>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <omp.h>

static const int N = 20;              // Number of integrate to compute
static const int CHUNKSIZE = 1;       // Defines the chunk size as 1 contiguous iteration
static const double DELTA = 0.00000001;

//////////////////////////////////////////

// Compute exact value of F(x) = x³/3
double F(double x) {
    return pow(x, 3) / 3.0;
}

// Numerical computation of F(x) : integ[a,b] x² dx
double num_F(double b) {
    double a = 0.0;
    double y = 0.0;

    for(double x=a ; x<b ; x+=DELTA) {
        y += x * x * DELTA;
    }

    return y;
}

//////////////////////////////////////////

void print_tab(const double (& t)[N])
{
    for(int i=0 ; i<N ; i++) {
        std::cout << std::fixed;
        std::cout << "num_F(" << i << ") = " << t[i] << " - F(" << i << ") = " << F(i) << std::endl;
    }
}

//////////////////////////////////////////

int main()
{
    double x[N], y[N];

    // Init x and y
    for(int i=0 ; i<N ; i++) {
        x[i] = i;
        y[i] = 0;
    }

    boost::posix_time::ptime start_time = boost::posix_time::microsec_clock::local_time();
    double omp_start_time = omp_get_wtime();

    // Forks off the threads
    #pragma omp parallel
    {
        // Starts the work sharing construct (static / dynamic)
        #pragma omp for schedule(dynamic, CHUNKSIZE)
        for(int i = 0 ; i < N ; i++)
            y[i] = num_F(x[i]);
    }

    boost::posix_time::ptime end_time = boost::posix_time::microsec_clock::local_time();
    boost::posix_time::time_duration delta_time = end_time - start_time;
    double omp_end_time = omp_get_wtime();
    double omp_delta_time = omp_end_time - omp_start_time;

    // Print y
    print_tab(y);

    // Print delta_time
    std::cerr << "boost : " << delta_time << std::endl;
    std::cerr << "omp   : " << omp_delta_time << std::endl;

    return 0;
}
