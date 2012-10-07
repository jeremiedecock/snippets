#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>

class Foo {
    private:
    double * num;

    public:
    Foo(double *);
    void incrementNum();
};

#endif // CLASSES_H
