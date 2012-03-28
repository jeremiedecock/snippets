#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Point> point_wrapper("Point", boost::python::init<double, double>());
    point_wrapper.def(boost::python::init<>());                // 2nd constructor
    point_wrapper.def("get_x", &Point::getX, "Get x value.");
    point_wrapper.def("get_y", &Point::getY, "Get y value.");
    point_wrapper.def("set_x", &Point::setX, "Set x value.");
    point_wrapper.def("set_y", &Point::setY, "Set y value.");
    point_wrapper.def("to_string", &Point::toString, "Get string representation."); // TODO: use something more pythonic...
    point_wrapper.def_readwrite("color", &Point::color, "Color value.");
    //point_wrapper.def_readwrite("cpt", &Point::cpt, "");
}
