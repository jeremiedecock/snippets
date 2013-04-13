/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c random.cc
 *    g++ -o random random.o -lsfml-system
 *
 * SEE:
 *    http://www.sfml-dev.org/tutorials/1.6/system-random.php
 */

#include <iostream>
#include <time.h>
#include <SFML/System.hpp>

int main()
{
    unsigned int seed = time(NULL);
    sf::Randomizer::SetSeed(seed);

    // Generate random integers between 0 and 100
    for(int i=0 ; i<10 ; i++) {
        int random = sf::Randomizer::Random(0, 100);
        std::cout << random << std::endl;
    }

    // Generate random floats between -1.0 and +1.0
    for(int i=0 ; i<10 ; i++) {
        float random = sf::Randomizer::Random(-1.f, 1.f);
        std::cout << random << std::endl;
    }
    
    return 0;
}
