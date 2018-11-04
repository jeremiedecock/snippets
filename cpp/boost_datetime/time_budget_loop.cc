/* 
 * Chrono: measure time duration between two points with boost.datetime
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.datetime library
 * Usage: g++ time_budget_loop.cc
 *
 */

#include <iostream>
#include <boost/date_time/posix_time/posix_time.hpp>

int main() {

    double wait_seconds = 0.005;
    boost::posix_time::ptime end_time = boost::posix_time::microsec_clock::local_time() + boost::posix_time::microseconds(wait_seconds * 1000000.);

    while(boost::posix_time::microsec_clock::local_time() < end_time) {
        // do something
        std::cout << boost::posix_time::microsec_clock::local_time() << std::endl;
    }

    return 0;
}
