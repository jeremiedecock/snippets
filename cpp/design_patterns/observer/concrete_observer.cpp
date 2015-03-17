/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "concrete_observer.h"
#include "concrete_subject.h"

#include <iostream>

void ConcreteObserver::update(Subject * updated_subject) {
    std::cout << this << " " << dynamic_cast<ConcreteSubject *>(updated_subject)->getState() << std::endl; // TODO
}
