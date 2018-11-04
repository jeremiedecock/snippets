#ifndef CLASSES_H
#define CLASSES_H

#include <string>

// Base class /////////////////////////

class Hello {
    public:
        virtual void message();
        std::string getName();
};

#endif // CLASSES_H
