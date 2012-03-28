#ifndef classes_h
#define classes_h

#include <iostream>

// Basic classes
class Point {
    private:
        double x;
        double y;

    public:
        Point(double, double);
        Point();

        double getX();
        double getY();

        void setX(double);
        void setY(double);
};

#endif // classes_h
