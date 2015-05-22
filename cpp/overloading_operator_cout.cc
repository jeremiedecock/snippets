#include <iostream>

// point.h
class Point
{
    public:
        double x, y;

    public:
        Point(double _x, double _y) {
            this->x = _x;
            this->y = _y;
        }

        friend std::ostream & operator << (std::ostream &, const Point &);
};

// point.cc
std::ostream & operator << (std::ostream & os, const Point & p)
{
    os << p.x << "," << p.y;
    return os;
}

// main.cc
int main()
{
    Point p(1., 2.);

    std::cout << p << std::endl;
}
