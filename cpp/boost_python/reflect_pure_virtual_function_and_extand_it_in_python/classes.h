#ifndef CLASSES_H
#define CLASSES_H

#include <string>

// Base class /////////////////////////

class Hello {
    public:
        virtual void message() = 0;
        std::string getName();
};

#endif // CLASSES_H
