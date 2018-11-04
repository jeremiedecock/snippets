#include "classes.h"

#include <iostream>

// Basic classes ////////////////////////////////////////////////////////////

Hello::Hello(std::string name) {
    std::cout << "Making an Hello object for " << name << "..." << std::endl;
    this->name = name;
}

void Hello::greet() {
    std::cout << "Hello " << this->name << "!" << std::endl;
}

