/*
 * A very basic demo of SFML.
 *
 * REQUIRE:
 *    libsfml-dev (Debian)
 *
 * USAGE:
 *    g++ -c image.cc
 *    g++ -o image image.o -lsfml-graphics -lsfml-window -lsfml-system
 * 
 * SEE:
 *    http://www.sfml-dev.org/tutorials/1.6/graphics-sprite-fr.php
 */

#include <iostream>
#include <iomanip>
#include <SFML/Graphics.hpp>

int main()
{
    // PRINT AND UPDATE AN IMAGE FROM A FILE //////////////

    std::string filename1("image.png");

    sf::Image image1;
    if(!image1.LoadFromFile(filename1)) {
        // Error...
        std::cerr << filename1 << ": wrong image file." << std::endl;
    }

    std::cout << filename1
              << " (" << image1.GetWidth() << "x"
              << image1.GetHeight() << ")" << std::endl;

    for(unsigned int x=0 ; x < image1.GetWidth()/2 ; x++) {
        for(unsigned int y=0 ; y < image1.GetHeight()/2 ; y++) {
            // Rem: color.r, color.g, ... are unsigned char; they have to be
            // casted to print numbers.
            sf::Color color = image1.GetPixel(x, y);
            std::cout << std::setfill('0')
                      << "(" << std::setw(3) << static_cast<int>(color.r)
                      << "," << std::setw(3) << static_cast<int>(color.g)
                      << "," << std::setw(3) << static_cast<int>(color.b)
                      << "," << std::setw(3) << static_cast<int>(color.a)
                      << ") ";
        }
        std::cout << std::endl;
    }

    // Invert pixels value
    for(unsigned int x=0 ; x < image1.GetWidth() ; x++) {
        for(unsigned int y=0 ; y < image1.GetHeight() ; y++) {
            sf::Color former_color = image1.GetPixel(x, y);
            
            sf::Color new_color(255, 255, 255);
            new_color.r = new_color.r - former_color.r;
            new_color.g = new_color.g - former_color.g;
            new_color.b = new_color.b - former_color.b;
            new_color.a = former_color.a;

            image1.SetPixel(x, y, new_color);
        }
    }

    // Save invert image
    image1.SaveToFile(filename1);

    // CREATE A NEW IMAGE /////////////////////////////////
    
    std::string filename2("new_image.png");

    unsigned int seed = time(NULL);
    sf::Randomizer::SetSeed(seed);

    sf::Image image2(200, 200, sf::Color(255, 255, 255));

    for(unsigned int x=0 ; x < image2.GetWidth() ; x++) {
        for(unsigned int y=0 ; y < image2.GetHeight() ; y++) {
            sf::Color color(sf::Randomizer::Random(0, 255), sf::Randomizer::Random(0, 255), sf::Randomizer::Random(0, 255));
            image2.SetPixel(x, y, color);
        }
    }

    image2.SaveToFile(filename2);

    return 0;
}
