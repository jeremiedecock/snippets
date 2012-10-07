/* 
 * Time_string_conversion: print datetime
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.datetime library
 * Usage: g++ time_string_conversion.cc -lboost_date_time
 *
 */

#include <iostream>
#include <string>
#include <boost/date_time/posix_time/posix_time.hpp>

int main() {

    /* Get the current time from the clock (one second resolution) */
    boost::posix_time::ptime now = boost::posix_time::second_clock::local_time();
    //boost::posix_time::ptime now = boost::posix_time::second_clock::universal_time();

    /* Convert the ptime object to a string */
    std::cout << boost::posix_time::to_simple_string(now) << std::endl;
    std::cout << boost::posix_time::to_iso_string(now) << std::endl;
    std::cout << boost::posix_time::to_iso_extended_string(now) << std::endl;

    /* Get the date part out of the time */
    boost::gregorian::date today = now.date();
    std::cout << today << std::endl;

    /* Set the time from a string */
    std::string time_string("20020131T235959");

    boost::posix_time::ptime posix_time(boost::posix_time::from_iso_string(time_string));
    std::cout << posix_time.date() << posix_time.time_of_day() << std::endl;

    return 0;
}

