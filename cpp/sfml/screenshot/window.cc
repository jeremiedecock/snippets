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
 *    http://www.sfml-dev.org/tutorials/1.6/graphics-window.php
 */

#include <iostream>
#include <SFML/Graphics.hpp>

int main()
{
    sf::RenderWindow window(sf::VideoMode(320, 200, 24), "SFML Window");

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

            // 'F1' key pressed -> screenshot
            if((event.Type == sf::Event::KeyPressed) && (event.Key.Code == sf::Key::F1)) {
                sf::Image screen = window.Capture();
                screen.SaveToFile("screenshot.jpg");
            }
        }

        // Clear the window (with white pixels)
        window.Clear(sf::Color(255, 0, 0));

        // Display
        window.Display();
    }

    return 0;
}
