#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<Point2D> point2d_wrapper("Point2D", boost::python::init<double, double>());
    point2d_wrapper.def("get_x", &Point2D::getX, "Get x value.");
    point2d_wrapper.def("get_y", &Point2D::getY, "Get y value.");
    point2d_wrapper.def("set_x", &Point2D::setX, "Set x value.");
    point2d_wrapper.def("set_y", &Point2D::setY, "Set y value.");
    point2d_wrapper.def("to_string", &Point2D::toString, "Get string representation."); // TODO: use something more pythonic...

    boost::python::class_< Point3D, boost::python::bases<Point2D> > point3d_wrapper("Point3D", boost::python::init<double, double, double>());
    point3d_wrapper.def("get_z", &Point3D::getZ, "Get z value.");
    point3d_wrapper.def("set_z", &Point3D::setZ, "Set z value.");
    point3d_wrapper.def("to_string", &Point3D::toString, "Get string representation."); // TODO: use something more pythonic...
}
