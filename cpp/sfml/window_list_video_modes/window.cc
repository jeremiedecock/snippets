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
    std::cout << "Available modes (mostly usefull with fullscreen mode):" << std::endl;

    unsigned int video_modes_count = sf::VideoMode::GetModesCount();

    for(unsigned int i = 0 ; i < video_modes_count ; ++i) {
        sf::VideoMode mode = sf::VideoMode::GetMode(i);

        std::cout << "mode " << i << ": " << mode.Width << "x" << mode.Height << " (" << mode.BitsPerPixel << " bits)" << std::endl;
    }

    std::cout << "\"Best\" mode is \"mode 0\"" << std::endl;

    return 0;
}
