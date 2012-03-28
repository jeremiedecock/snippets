#ifndef functions_h
#define functions_h

#include <iostream>

// Basic functions
void print_on_cout();
double one_argument(double);
double two_arguments(int, double);

// Strings
std::string std_string(std::string);
char const * c_string(char *);

// Exceptions
std::string throw_exception(int);

#endif // functions_h
