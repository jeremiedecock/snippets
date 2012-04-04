#include "classes.h"
#include <iostream>

class HelloFr : public Hello
{
    public:
        // MANDATORY !
        HelloFr(std::string _name) : Hello(_name) { }
};

int main()
{
    Hello msg1(std::string("Bob"));

    HelloFr msg2(std::string("Joe"));

    return 0;
}
