/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef CONCRETE_OBSERVER_H
#define CONCRETE_OBSERVER_H

#include "observer.h"

class ConcreteObserver : public Observer {
    public:
        void update(Subject * updated_subject);
};

#endif // CONCRETE_OBSERVER_H
