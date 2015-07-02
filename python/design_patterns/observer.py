#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# See "Python, Petit guide à l'usage du développeur agile", Tarek Ziadé, Ed. Dunod (2007)

class Observable(object):
    """The subject."""

    def __init__(self):
        raise NotImplementedError

    def register(self, observer):
        self.observers.add(observer)

    def unregister(self, observer):
        try:
            self.observers.remove(observer)
        except KeyError:
            pass

    def notify(self):
        for observer in self.observers:
            observer.update(self)


class ConcreteObservable(Observable):
    """The concrete subject."""

    def __init__(self):
        self.observers = set()
        self.state = 0

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        self.notify()


class Observer(object):
    
    def update(self, observable):
        raise NotImplementedError


class ConcreteObserver(Observer):

    def update(self, observable):
        print(id(self), observable.getState())


def main():
    observable = ConcreteObservable()
    observer1 = ConcreteObserver()
    observer2 = ConcreteObserver()

    observable.setState(0)
    observable.register(observer1)
    observable.setState(1)
    observable.register(observer2)
    observable.setState(2)
    observable.unregister(observer1)
    observable.setState(3)
    observable.unregister(observer2)
    observable.setState(4)

if __name__ == '__main__':
    main()
