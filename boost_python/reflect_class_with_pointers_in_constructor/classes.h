#ifndef CLASSES_H
#define CLASSES_H

#include <iostream>

// MuttableNumbers

class MuttableNumber {
    public:
    double value;
};

// Foo

class Foo {
    private:
    MuttableNumber * num;

    public:
    Foo(MuttableNumber *);
    void incrementNum();
};

#endif // CLASSES_H
