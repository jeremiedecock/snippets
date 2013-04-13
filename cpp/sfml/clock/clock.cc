/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c clock.cc
 *    g++ -o clock clock.o -lsfml-system
 *
 * SEE:
 *    http://www.sfml-dev.org/tutorials/1.6/window-time.php
 */

#include <iostream>
#include <SFML/System.hpp>

int main()
{
    sf::Clock clock;

    std::cout << "Measurement without reset:" << std::endl;
    while(clock.GetElapsedTime() < 5.0) {
        sf::Sleep(0.5);
        std::cout << clock.GetElapsedTime() << std::endl;
    }

    clock.Reset();

    std::cout << "Measurement with reset:" << std::endl;
    for(int i=0 ; i < 5 ; i++) {
        sf::Sleep(0.5);
        std::cout << clock.GetElapsedTime() << std::endl;
        clock.Reset();
    }

    return 0;
}
