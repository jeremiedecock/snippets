/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c clock.cc
 *    g++ -o clock clock.o -lsfml-system
 */

#include <iostream>
#include <SFML/System.hpp>

int main()
{
    sf::Clock Clock;

    while(Clock.GetElapsedTime() < 5.0) {
        std::cout << Clock.GetElapsedTime() << std::endl;
        sf::Sleep(0.5);
    }

    return 0;
}
