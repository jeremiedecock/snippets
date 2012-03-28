#include <boost/python.hpp>
#include "functions.h"

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::def("print_on_cout", print_on_cout, "a function without argument and return value that print on cout");
    boost::python::def("one_argument", one_argument, "a function with one argument");
    boost::python::def("two_arguments", two_arguments, "a function with two arguments");
    boost::python::def("std_string", std_string, "a function which handle std::string");
    boost::python::def("c_string", c_string, "a function which handle C strings");
    boost::python::def("throw_exception", throw_exception, "a function which may throw an exception");
}
