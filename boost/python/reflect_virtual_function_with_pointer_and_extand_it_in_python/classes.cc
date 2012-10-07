#include "classes.h"

//////////

Point::Point(double _x, double _y) {
    this->x = _x;
    this->y = _y;
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

//////////

void Geometry::translate(Point * point) {
    point->setX( point->getX() + this->getTranslateValue() );
    point->setY( point->getY() + this->getTranslateValue() );
}

double Geometry::getTranslateValue() {
    return 2.0;
}

