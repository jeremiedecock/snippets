#include "classes.h"

#include <iostream>

// Basic classes ////////////////////////////////////////////////////////////

Hello::Hello() {
    std::cout << "Making an Hello object..." << std::endl;
}

void Hello::greet() {
    std::cout << "Hello!" << std::endl;
}

