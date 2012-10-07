/* 
 * Chrono: measure time duration between two points with boost.datetime
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.chrono and boost.system library
 * Usage: g++ chrono.cc -lboost_chrono -lboost_system -o chrono
 *
 */

#include <boost/chrono.hpp>
#include <cmath>
#include <iostream>

int main()
{
    boost::chrono::system_clock::time_point start = boost::chrono::system_clock::now();

    // Do something...
    for(double x=0.0 ; x<10.0 ; x+=0.0000001) {
        double y = std::sqrt(x);
    }

    boost::chrono::duration<double> sec = boost::chrono::system_clock::now() - start;

    std::cout << "Took " << sec.count() << " seconds" << std::endl;
}
