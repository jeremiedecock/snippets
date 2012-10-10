#include "classes.h"
#include <iostream>

void Hello::message() {
    std::cout << "Hello " << this->getName() << " !" << std::endl;
}

std::string Hello::getName() {
    return std::string("John");
}

