#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Hello> hello_wrapper("Hello", boost::python::init<>()); // First constructor
    hello_wrapper.def(boost::python::init<std::string>());                        // Second constructor
    hello_wrapper.def("greet", &Hello::greet, "Print a message");
}
