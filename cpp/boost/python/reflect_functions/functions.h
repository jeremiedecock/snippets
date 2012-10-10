#ifndef functions_h
#define functions_h

#include <iostream>

// Basic functions
void print_on_cout();
double one_argument(double);
double two_arguments(int, double);

// Overloading
std::string overload_arguments(double x);
std::string overload_arguments(double x, int n);
void overload_arguments();
void overload_arguments(std::string s);

// Default arguments
void default_arguments(double x, double y=0, double z=0);

// Strings
std::string std_string(std::string);
char const * c_string(char *);

// Exceptions
std::string throw_exception(int);

#endif // functions_h
