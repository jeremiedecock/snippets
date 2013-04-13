/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c window.cc
 *    g++ -o window window.o -lsfml-window -lsfml-system
 * 
 * SEE:
 *    http://www.sfml-dev.org/tutorials/1.6/window-window.php
 */

#include <iostream>
#include <SFML/Window.hpp>

int main()
{
    sf::Window window(sf::VideoMode(640, 480, 24), "SFML Window");

    // Main Loop
    bool running = true;
    while(running) {
        window.Display();
    }

    return 0;
}
