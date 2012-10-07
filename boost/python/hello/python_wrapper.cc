#include <boost/python.hpp>
#include "functions.h"

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::def("pyhello", hello, "a function without argument and return value that print on cout");
}

