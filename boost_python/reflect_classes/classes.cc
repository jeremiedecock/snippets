#include "classes.h"

// Basic classes ////////////////////////////////////////////////////////////

Point::Point(double _x, double _y) {
    this->x = _x;
    this->y = _y;
}

Point::Point() {
    this->x = 0;
    this->y = 0;
}

double Point::getX() {
    return this->x;
}

double Point::getY() {
    return this->y;
}

void Point::setX(double _x) {
    this->x = _x;
}

void Point::setY(double _y) {
    this->y = _y;
}

