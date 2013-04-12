/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c window.cc
 *    g++ -o window window.o -lsfml-window -lsfml-system
 */

#include <iostream>
#include <SFML/Window.hpp>

int main()
{
    sf::Window window(sf::VideoMode(320, 200, 24), "SFML Window");

    const sf::Input & input = window.GetInput();

    // Main Loop
    while(window.IsOpened()) {
        
        // Events
        sf::Event event;
        while(window.GetEvent(event)) {
            // 'Esc' key pressed
            if((event.Type == sf::Event::KeyPressed) && (event.Key.Code == sf::Key::Escape)) {
                window.Close();
            }
        }

        // Real time inputs
        if(input.IsKeyDown(sf::Key::Left)) {
            std::cout << "Left" << std::endl;
        }

        if(input.IsKeyDown(sf::Key::Right)) {
            std::cout << "Right" << std::endl;
        }

        if(input.IsKeyDown(sf::Key::Up)) {
            std::cout << "Up" << std::endl;
        }

        if(input.IsKeyDown(sf::Key::Down)) {
            std::cout << "Down" << std::endl;
        }

        // Display
        window.Display();
    }

    return 0;
}
