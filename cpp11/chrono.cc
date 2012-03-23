/* 
 * Chrono: measure time duration between two points with std::chrono
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Usage
 * Gcc >= 4.7: g++ -std=c++11 chrono.cc
 * Gcc  < 4.7: g++ -std=c++0x chrono.cc
 *
 */

#include <chrono>
#include <iostream>

int main()
{
    auto t1 = std::chrono::system_clock::now();
    usleep(100000);
    auto t2 = std::chrono::system_clock::now();

    std::cout << (t2 - t1).count() << std::endl;

    return 0;
}
