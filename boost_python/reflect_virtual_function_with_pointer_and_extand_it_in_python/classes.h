#ifndef CLASSES_H
#define CLASSES_H

// Point class ////////////////////////

class Point
{
    private:
        double x, y;

    public:
        Point(double, double);
        double getX();
        double getY();
        void setX(double);
        void setY(double);
};

// Base class /////////////////////////

class Geometry
{
    public:
        virtual void translate(Point * point);
        double getTranslateValue();
};

#endif // CLASSES_H
