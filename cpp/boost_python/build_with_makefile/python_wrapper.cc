#include <boost/python.hpp>
#include "func.h"

BOOST_PYTHON_MODULE(cppfunc)
{
    boost::python::def("square", square, "square function");
}
