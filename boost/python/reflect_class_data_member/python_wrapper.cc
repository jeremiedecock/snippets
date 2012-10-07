#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Point> point_wrapper("Point");
    point_wrapper.def_readwrite("x", &Point::x, "X value.");
    point_wrapper.def_readwrite("y", &Point::y, "Y value.");
}
