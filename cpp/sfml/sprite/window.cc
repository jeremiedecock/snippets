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
const int NUM_SPRITES = 15;

int main()
{
    unsigned int seed = time(NULL);
    sf::Randomizer::SetSeed(seed);

    std::string filename("image.png");

    // Load the sprite image from a file
    sf::Image image;
    if(!image.LoadFromFile(filename)) {
        // Error...
        std::cerr << filename << ": wrong image file." << std::endl;
    }
    //image.SetSmooth(false);

    // Create sprites
    std::vector<sf::Sprite> sprite_vec;
    for(int i=0 ; i<NUM_SPRITES ; i++) {
        sf::Sprite sprite(image);

        sprite.SetPosition(sf::Randomizer::Random(0, WIDTH), sf::Randomizer::Random(0, HEIGHT));
        sprite.SetRotation(sf::Randomizer::Random(-180.0f, 180.0f));
        sprite.SetScale(sf::Randomizer::Random(0.5f, 2.0f), sf::Randomizer::Random(0.5f, 2.0f));

        sprite_vec.push_back(sprite);
    }

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

        // Display sprite in our window
        for(int i=0 ; i<NUM_SPRITES ; i++) {
            window.Draw(sprite_vec[i]);
        }

        // Display
        window.Display();

    }

    return 0;
}
