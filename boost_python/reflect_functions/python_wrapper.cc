#include <boost/python.hpp>
#include "functions.h"

// Introduce some member function pointer variables for "overload_arguments"
std::string (*overload_arguments_1)(double) = overload_arguments;      // or "... = &overload_arguments;"
std::string (*overload_arguments_2)(double, int) = overload_arguments; // or "... = &overload_arguments;"
void (*overload_arguments_3)() = overload_arguments;                   // or "... = &overload_arguments;"
void (*overload_arguments_4)(std::string) = overload_arguments;        // or "... = &overload_arguments;"

// Write "thin wrappers" for "default_arguments"
// It's also possible to use "pointer variables" technique like for "overload_arguments"
void default_arguments_1(double x) { default_arguments(x); }
void default_arguments_2(double x, double y) { default_arguments(x, y); }
//void default_arguments_3(double x, double z) { default_arguments(x, z=z); }

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::def("print_on_cout", print_on_cout, "a function without argument and return value that print on cout");
    boost::python::def("one_argument", one_argument, "a function with one argument");
    boost::python::def("two_arguments", two_arguments, "a function with two arguments");

    boost::python::def("overload_arguments", overload_arguments_1, "a function with overloaded arguments");
    boost::python::def("overload_arguments", overload_arguments_2, "a function with overloaded arguments");
    boost::python::def("overload_arguments", overload_arguments_3, "a function with overloaded arguments");
    boost::python::def("overload_arguments", overload_arguments_4, "a function with overloaded arguments");

    boost::python::def("default_arguments", default_arguments, "a function with default arguments");
    boost::python::def("default_arguments", default_arguments_1, "a function with default arguments");
    boost::python::def("default_arguments", default_arguments_2, "a function with default arguments");
    //boost::python::def("default_arguments", default_arguments_3, "a function with default arguments");

    boost::python::def("std_string", std_string, "a function which handle std::string");
    boost::python::def("c_string", c_string, "a function which handle C strings");

    boost::python::def("throw_exception", throw_exception, "a function which may throw an exception");
}
