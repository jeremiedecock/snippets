#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Point> point_wrapper("Point");
    point_wrapper.def_readwrite("x", &Point::x, "x");
    point_wrapper.def_readwrite("y", &Point::y, "y");

    boost::python::class_<Foo> foo_wrapper("Foo", boost::python::init<Point *>());
    foo_wrapper.def("translate", &Foo::translate, "Translate the point.");
}
