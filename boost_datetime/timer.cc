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

    for(int i=0 ; i<10 ; i++) {
        double wait_seconds = 1;
        boost::posix_time::ptime end_time = boost::posix_time::microsec_clock::local_time() + boost::posix_time::microseconds(wait_seconds * 1000000.);

        while(boost::posix_time::microsec_clock::local_time() < end_time) {
            // do nothing
        }

        std::cout << end_time << std::endl;
    }

    return 0;
}
