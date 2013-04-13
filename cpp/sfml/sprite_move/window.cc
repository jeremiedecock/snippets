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
const int ROT_SPEED = 5;
const int NUM_SPRITES = 10;

int main()
{
    std::string filename("image.png");

    // Load the sprite image from a file
    sf::Image image;
    if(!image.LoadFromFile(filename)) {
        // Error...
        std::cerr << filename << ": wrong image file." << std::endl;
    }

    // Create sprites
    std::vector<sf::Sprite> sprite_vec;
    for(int i=0 ; i<NUM_SPRITES ; i++) {
        sf::Sprite sprite(image);

        sprite.SetPosition(sf::Randomizer::Random(0, WIDTH), sf::Randomizer::Random(0, HEIGHT));
        sprite.SetCenter(sprite.GetSize().y/2., sprite.GetSize().x/2.);
        sprite.SetRotation(sf::Randomizer::Random(-180.0f, 180.0f));
        float scale = sf::Randomizer::Random(0.5f, 1.5f);
        sprite.SetScale(scale, scale);

        sprite_vec.push_back(sprite);
    }

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

            // 'F1' key pressed -> screenshot
            if((event.Type == sf::Event::KeyPressed) && (event.Key.Code == sf::Key::F1)) {
                sf::Image screen = window.Capture();
                screen.SaveToFile("screenshot.jpg");
            }
        }

        // Update sprites
        for(int i=0 ; i<NUM_SPRITES ; i++) {
            sprite_vec[i].Move(0, SPEED * window.GetFrameTime());
            sprite_vec[i].Rotate(ROT_SPEED);

            // If the sprite i is out of the screen
            if(sprite_vec[i].GetPosition().y > HEIGHT + sprite_vec[i].GetSize().y) {
                sprite_vec[i].SetX(sf::Randomizer::Random(0, WIDTH));
                sprite_vec[i].SetY(-sprite_vec[i].GetSize().y);

                sprite_vec[i].SetRotation(sf::Randomizer::Random(-180.0f, 180.0f));
                float scale = sf::Randomizer::Random(0.5f, 1.5f);
                sprite_vec[i].SetScale(scale, scale);
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
