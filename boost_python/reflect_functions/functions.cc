#include "functions.h"
#include <stdexcept>
#include <cstring>

void print_on_cout() {
    std::cout << "hello";
}

double one_argument(double x) {
    return x * x;
}

double two_arguments(int n, double x) {
    return n * x;
}

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

std::string throw_exception(int n) {
    std::string str_tab[] = {std::string("msg1"), std::string("msg2"), std::string("msg3")};

    if(n>2) {
        throw std::range_error("throw_exception: index out of range");
    }

    return str_tab[n];
}

