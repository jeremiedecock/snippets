#!/usr/bin/env groovy

// Usage: groovy class.groovy
//    or: ./class.groovy

class Foo {
    void hello() {
        System.out.println("Hello, World!")
    }
}

Foo f = new Foo();

f.hello();
