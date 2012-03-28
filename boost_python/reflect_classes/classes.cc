#include "classes.h"
#include <sstream>

// Basic classes ////////////////////////////////////////////////////////////

int Point::cpt = 0;

Point::Point(double _x, double _y) {
    this->x = _x;
    this->y = _y;
    Point::cpt++;
}

Point::Point() {
    this->x = 0;
    this->y = 0;
    Point::cpt++;
}

double Point::getX() const {
    return this->x;
}

double Point::getY() const {
    return this->y;
}

void Point::setX(double _x) {
    this->x = _x;
}

void Point::setY(double _y) {
    this->y = _y;
}

std::string Point::toString() {
    std::ostringstream oss;
    oss << "(" << this->getX() << "," << this->getY() << ") " << this->color;
    return oss.str();
}

