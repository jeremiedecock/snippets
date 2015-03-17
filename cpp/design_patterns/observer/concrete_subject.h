/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef CONCRETE_SUBJECT_H
#define CONCRETE_SUBJECT_H

#include "subject.h"

#include <string>

class ConcreteSubject : public Subject {
    private:
        std::string state;

    public:
        std::string getState() const;

        void setState(std::string state);
};

#endif // CONCRETE_SUBJECT_H
