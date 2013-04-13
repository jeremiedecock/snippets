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
 *    http://www.sfml-dev.org/tutorials/1.6/graphics-shape.php
 */

#include <iostream>
#include <SFML/Graphics.hpp>

const int WIDTH = 640;
const int HEIGHT = 480;

int main()
{
    // Create shapes
    sf::Shape line   = sf::Shape::Line(10., 10., 500., 200., 1., sf::Color(255, 0, 0));
    sf::Shape circle = sf::Shape::Circle(300., 300., 100., sf::Color(0, 255, 0));
    sf::Shape rect   = sf::Shape::Rectangle(30., 100., 200., 200., sf::Color(0, 0, 255));

    //////////

    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT, 24), "SFML Window");

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
        }

        // Clear the window (with white pixels)
        window.Clear(sf::Color(255, 255, 255));

        // Display shapes in our window
        window.Draw(line);
        window.Draw(circle);
        window.Draw(rect);

        // Display
        window.Display();

    }

    return 0;
}
