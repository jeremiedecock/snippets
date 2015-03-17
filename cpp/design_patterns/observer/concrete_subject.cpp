/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "concrete_subject.h"

std::string ConcreteSubject::getState() const {
    return this->state;
}

void ConcreteSubject::setState(std::string state) {
    this->state = state;
    this->notify();
}

