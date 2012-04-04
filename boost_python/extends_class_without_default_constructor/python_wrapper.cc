#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Hello> hello_wrapper("Hello", boost::python::init<std::string>());
}
