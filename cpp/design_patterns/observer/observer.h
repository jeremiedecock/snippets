/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef OBSERVER_H
#define OBSERVER_H

class Subject;

class Observer {
    //protected:
    //    Observer(); // TODO

    public:
        virtual ~Observer() {};

        virtual void update(Subject * updated_subject) = 0;
};

#endif // OBSERVER_H
