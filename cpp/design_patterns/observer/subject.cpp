/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "subject.h"
#include "observer.h"

#include <iostream>

void Subject::attach(Observer * p_observer) {
    this->observerSet.insert(p_observer);
    std::cout << "attach " << p_observer << std::endl;
}

void Subject::detach(Observer * p_observer) {
    this->observerSet.erase(p_observer);
    std::cout << "detach " << p_observer << std::endl;
}

void Subject::notify() {
    std::set<Observer *>::iterator it;
    for(it = this->observerSet.begin() ; it != this->observerSet.end() ; it++) {
        (*it)->update(this);
    }
}
