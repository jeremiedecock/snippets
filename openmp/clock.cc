#include <iostream>
#include <ctime>

#include <boost/date_time/posix_time/posix_time.hpp>

#include <omp.h>

#define N 4

void c_wait(double num_seconds) {
    clock_t end_wait;

    end_wait = clock() + num_seconds * CLOCKS_PER_SEC;

    while(clock() < end_wait) {
        // do nothing...
    }
}

// ATTENTION : num_seconds est un entier dans le constructeur boost::posix_time::seconds() => pour des durées < 1s, utiliser milliseconds() !!!
void boost_wait(long num_seconds) {
    //boost::posix_time::ptime end_wait = boost::posix_time::microsec_clock::local_time() + boost::posix_time::time_duration(0,0,num_seconds,0); // Ok
    boost::posix_time::ptime end_wait = boost::posix_time::microsec_clock::local_time() + boost::posix_time::seconds(num_seconds);

    while(boost::posix_time::microsec_clock::local_time() < end_wait) {
        // do nothing...
    }
}

int main(int argc, char *argv[])
{
    #pragma omp parallel
    {
        #pragma omp master
        {
            int nthreads = omp_get_num_threads();
            std::cout << "There are " << nthreads << " threads" << std::endl << std::endl;
        }
    }
    
    std::cout << "Using clock():" << std::endl;

    #pragma omp parallel
    {
        int th_id = omp_get_thread_num();

        double omp_start_time = omp_get_wtime();
        c_wait(N);
        double omp_end_time = omp_get_wtime();
        double omp_delta_time = omp_end_time - omp_start_time;

        #pragma omp critical
        {
            std::cout << "Thread " << th_id << ": expected wait time = " << N << "s; actual wait time=" << omp_delta_time << "s" << std::endl;
        }
    }

    std::cout << std::endl << "Using boost::posix_time::microsec_clock::local_time():" << std::endl;

    #pragma omp parallel
    {
        int th_id = omp_get_thread_num();

        double omp_start_time = omp_get_wtime();
        boost_wait(N);
        double omp_end_time = omp_get_wtime();
        double omp_delta_time = omp_end_time - omp_start_time;

        #pragma omp critical
        {
            std::cout << "Thread " << th_id << ": expected wait time = " << N << "s; actual wait time=" << omp_delta_time << "s" << std::endl;
        }
    }

    return 0;
}
