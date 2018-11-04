#ifndef classes_h
#define classes_h

#include <string>

// Base class

class Point2D {
    private:
        double x;
        double y;

    public:
        Point2D(double, double);

        double getX() const;
        double getY() const;

        void setX(double);
        void setY(double);

        std::string toString();
};

// Derived class

class Point3D : public Point2D {
    private:
        double z;

    public:
        Point3D(double, double, double);

        double getZ() const;
        void setZ(double);

        std::string toString();
};

#endif // classes_h
