/* 
 * ...
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "concrete_subject.h"
#include "concrete_observer.h"

int main() {
    ConcreteSubject  concrete_subject;

    ConcreteObserver concrete_observer1;
    ConcreteObserver concrete_observer2;

    concrete_subject.attach(&concrete_observer1);
    concrete_subject.attach(&concrete_observer2);

    concrete_subject.setState("tic");
    concrete_subject.setState("tac");

    concrete_subject.detach(&concrete_observer1);

    concrete_subject.setState("tic");
    concrete_subject.setState("tac");

    concrete_subject.detach(&concrete_observer2);
    
    return 0;
}
