#include "classes.h"

Foo::Foo(MuttableNumber * _num) {
    this->num = _num;
}

void Foo::incrementNum() {
    this->num->value += 1;
}
