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
 *    http://www.sfml-dev.org/tutorials/1.6/graphics-sprite.php
 */

#include <iostream>
#include <SFML/Graphics.hpp>

const int WIDTH = 640;
const int HEIGHT = 480;
const int SPEED = 150;

int main()
{
    std::string filename("image.png");

    // Load the sprite image from a file
    sf::Image image;
    if(!image.LoadFromFile(filename)) {
        // Error...
        std::cerr << filename << ": wrong image file." << std::endl;
    }
    image.SetSmooth(false);

    // Create sprite
    sf::Sprite sprite(image);
    sprite.SetPosition(WIDTH/2, HEIGHT/2);

    //////////

    sf::RenderWindow window(sf::VideoMode(WIDTH, HEIGHT, 24), "SFML Window");

    const sf::Input & input = window.GetInput();

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

        // Real time inputs
        if(input.IsKeyDown(sf::Key::Left)) {
            sprite.Move(-SPEED * window.GetFrameTime(), 0);
        }

        if(input.IsKeyDown(sf::Key::Right)) {
            sprite.Move(SPEED * window.GetFrameTime(), 0);
        }

        if(input.IsKeyDown(sf::Key::Up)) {
            sprite.Move(0, -SPEED * window.GetFrameTime());
        }

        if(input.IsKeyDown(sf::Key::Down)) {
            sprite.Move(0, SPEED * window.GetFrameTime());
        }

        // Clear the window (with white pixels)
        window.Clear(sf::Color(255, 255, 255));

        // Display sprite in our window
        window.Draw(sprite);

        // Display
        window.Display();

    }

    return 0;
}
