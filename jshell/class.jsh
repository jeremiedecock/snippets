//usr/bin/env jshell --execution local "$0" "$@"; exit $?

class Foo {
    void hello() {
        System.out.println("Hello, World!");
    }
}

Foo f = new Foo();

f.hello();

/exit
