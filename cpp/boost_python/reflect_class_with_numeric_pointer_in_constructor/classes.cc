#include "classes.h"

Foo::Foo(double * _num) {
    this->num = _num;
}

void Foo::incrementNum() {
    (* this->num) += 1;
}
