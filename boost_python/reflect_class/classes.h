#ifndef classes_h
#define classes_h

#include <iostream>
#include <string>

// Basic classes
class Point {
    private:
        double x;
        double y;

    public:
        static int cpt;    // TODO: unreachable...
        std::string color;

    public:
        Point(double, double);
        Point();

        double getX() const;
        double getY() const;

        void setX(double);
        void setY(double);

        std::string toString();
};

#endif // classes_h
