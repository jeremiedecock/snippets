/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef SUBJECT_H
#define SUBJECT_H

#include <set>

class Observer;

class Subject {
    private:
        std::set<Observer *> observerSet;

    //protected:
    //    Subject(); // TODO

    public:
        virtual ~Subject() {};

        virtual void attach(Observer * p_observer);

        virtual void detach(Observer * p_observer);

        virtual void notify();
};

#endif // SUBJECT_H
