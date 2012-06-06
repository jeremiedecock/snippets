#ifndef classes_h
#define classes_h

#include <string>

// Basic classes
class Hello {
    private:
        std::string name;

    public:
        Hello();
        Hello(std::string);
        void greet();
};

#endif // classes_h
