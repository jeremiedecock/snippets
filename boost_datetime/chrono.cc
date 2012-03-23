/* 
 * Chrono: measure time duration between two points with boost.datetime
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.datetime library
 * Usage: g++ chrono.cc
 *
 */

#include <iostream>
#include <boost/date_time/posix_time/posix_time.hpp>

int main() {

    boost::posix_time::ptime start_time = boost::posix_time::microsec_clock::local_time();

    // Do something...
    for(double x=0.0 ; x<10.0 ; x+=0.0000001) {
        double y = std::sqrt(x);
    }

    boost::posix_time::ptime end_time = boost::posix_time::microsec_clock::local_time();
    boost::posix_time::time_duration delta_time = end_time - start_time;

    std::cout << delta_time.total_milliseconds() << "ms" << std::endl;

    return 0;
}
