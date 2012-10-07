#include "classes.h"
#include <sstream>

// Base class ////////////////////////////////////////////////////////////

Point2D::Point2D(double _x, double _y) {
    this->x = _x;
    this->y = _y;
}

double Point2D::getX() const {
    return this->x;
}

double Point2D::getY() const {
    return this->y;
}

void Point2D::setX(double _x) {
    this->x = _x;
}

void Point2D::setY(double _y) {
    this->y = _y;
}

std::string Point2D::toString() {
    std::ostringstream oss;
    oss << "(" << this->getX() << "," << this->getY() << ")";
    return oss.str();
}

// Base class ////////////////////////////////////////////////////////////

Point3D::Point3D(double _x, double _y, double _z) : Point2D(_x, _y) {
    this->z = _z;
}

double Point3D::getZ() const {
    return this->z;
}

void Point3D::setZ(double _z) {
    this->z = _z;
}

std::string Point3D::toString() {
    std::ostringstream oss;
    oss << "(" << this->getX() << "," << this->getY() << "," << this->getZ() << ")";
    return oss.str();
}

