#include <boost/python.hpp>
#include "classes.h"

class GeometryWrapper : public Geometry, public boost::python::wrapper<Geometry>
{
    public:
        void translate(Point * point) {
            if(boost::python::override translate = this->get_override("translate")) {
                // WARNING: here, translate(Point *) doesn't return anything, so the wrapper neither.
                //          If translate(Point *) had returned something, we would have written:
                //          "return translate(Point *);"
                translate(point);
            } else {
                // WARNING: here, translate(Point *) doesn't return anything, so the wrapper neither.
                //          If translate(Point *) had returned something, we would have written:
                //          "return Geometry::translate(Point *);"
                Geometry::translate(point);
            }
        }

        void default_translate(Point * point) {
            // WARNING: here, translate(Point *) doesn't return anything, so the wrapper neither.
            //          If translate(Point *) had returned something, we would have written:
            //          "return this->Geometry::translate(Point *);"
            this->Geometry::translate(point);
        }
};

BOOST_PYTHON_MODULE(cppclasses)
{
    // Point class
    boost::python::class_<Point> point_wrapper("Point", boost::python::init<double, double>());
    point_wrapper.def("get_x", &Point::getX, "Get x value.");
    point_wrapper.def("get_y", &Point::getY, "Get y value.");
    point_wrapper.def("set_x", &Point::setX, "Set x value.");
    point_wrapper.def("set_y", &Point::setY, "Set y value.");
    
    // Geometry class
    boost::python::class_<GeometryWrapper, boost::noncopyable> geometry_wrapper("Geometry");
    geometry_wrapper.def("translate", &Geometry::translate, &GeometryWrapper::default_translate, "Translate the point.");
    geometry_wrapper.def("get_translate_value", &Geometry::getTranslateValue, "Get translate value.");
}
