#include "functions.h"
#include <sstream>
#include <stdexcept>
#include <cstring>
#include <cmath>

// Basic functions ////////////////////////////////////////////////////////////

void print_on_cout() {
    std::cout << "hello";
}

double one_argument(double x) {
    return x * x;
}

double two_arguments(int n, double x) {
    return n * x;
}


// Overloading ////////////////////////////////////////////////////////////////

std::string overload_arguments(double x) {
    std::ostringstream oss;
    oss << "arg1=" << x;
    return oss.str();
}

std::string overload_arguments(double x, int n) {
    std::ostringstream oss;
    oss << "arg1=" << x;
    oss << ", ";
    oss << "arg2=" << n;
    return oss.str();
}

void overload_arguments() {
    std::cout << "no argument";
}

void overload_arguments(std::string s) {
    std::cout << "arg1=" << s;
}


// Default arguments //////////////////////////////////////////////////////////

void default_arguments(double x, double y, double z) {
    std::cout << x << " " << y << " " << z;
}

// Strings ////////////////////////////////////////////////////////////////////

std::string std_string(std::string s) {
    return std::string("c++ got '") + s + std::string("'");
}

char const * c_string(char * s) {
    int size = strlen(s);
    for(int i=0 ; i<size ; i++) {
        s[i]++;
    }
    return s;
}

// Exceptions /////////////////////////////////////////////////////////////////

std::string throw_exception(int n) {
    std::string str_tab[] = {
        std::string("msg1"),
        std::string("msg2"),
        std::string("msg3")
    };

    if(n>2) {
        throw std::range_error("throw_exception: index out of range");
    }

    return str_tab[n];
}

