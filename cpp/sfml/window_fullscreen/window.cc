/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c window.cc
 *    g++ -o window window.o -lsfml-graphics -lsfml-window -lsfml-system
 *
 * SEE:
 *    http://www.sfml-dev.org/tutorials/1.6/window-window.php
 */

#include <iostream>
#include <SFML/Graphics.hpp>

int main()
{
    std::cout << "Available modes:" << std::endl;

    unsigned int video_modes_count = sf::VideoMode::GetModesCount();

    for(unsigned int i = 0 ; i < video_modes_count ; ++i) {
        sf::VideoMode mode = sf::VideoMode::GetMode(i);

        std::cout << "mode " << i << ": " << mode.Width << "x" << mode.Height << " (" << mode.BitsPerPixel << " bits)" << std::endl;
    }

    // See http://www.sfml-dev.org/tutorials/1.6/window-window.php
    std::cout << "Use the \"best\" mode: mode 0" << std::endl;
    sf::RenderWindow window(sf::VideoMode::GetMode(0), "SFML Window", sf::Style::Fullscreen);

    // Main Loop
    while(window.IsOpened()) {
        
        // Events
        sf::Event event;
        while(window.GetEvent(event)) {
            // Window closed
            if(event.Type == sf::Event::Closed) {
                window.Close();
            }

            // 'Esc' key pressed
            if((event.Type == sf::Event::KeyPressed) && (event.Key.Code == sf::Key::Escape)) {
                window.Close();
            }

            // 'q' key pressed
            if((event.Type == sf::Event::KeyPressed) && (event.Key.Code == sf::Key::Q)) {
                window.Close();
            }
        }
        
        // Clear the window (with red pixels)
        window.Clear(sf::Color(200, 0, 0));

        // Display
        window.Display();

    }
    
    return 0;
}
