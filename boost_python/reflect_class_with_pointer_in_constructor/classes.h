#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>

// MuttableNumbers

class Point {
    public:
    double x, y;
};

// Foo

class Foo {
    private:
    Point * pt;

    public:
    Foo(Point *);
    void translate();
};

#endif // CLASSES_H
