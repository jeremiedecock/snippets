#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Hello> hello_wrapper("Hello");
    hello_wrapper.def("greet", &Hello::greet, "Print a message");
}
