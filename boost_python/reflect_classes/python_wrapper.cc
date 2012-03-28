#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Point> point_wrapper("Point", boost::python::init<double, double>());
    point_wrapper.def(boost::python::init<>());
    point_wrapper.def("get_x", &Point::getX, "Get x value.");
    point_wrapper.def("get_y", &Point::getY, "Get y value.");
    point_wrapper.def("set_x", &Point::setX, "Set x value.");
    point_wrapper.def("set_y", &Point::setY, "Set y value.");
}
