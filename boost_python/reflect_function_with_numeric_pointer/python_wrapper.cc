#include <boost/python.hpp>
#include "functions.h"

// Fix muttable issue...

class MuttableDouble {
    public:
    double value;

    public:
    MuttableDouble() {};
    MuttableDouble(double x) : value(x) {};
};

void foo_wrapper(MuttableDouble * muttable_x) {
    double * x = &(muttable_x->value);
    foo(x);
}

// Define python module

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::class_<MuttableDouble> muttable_double_wrapper("MuttableDouble", boost::python::init<double>());
    muttable_double_wrapper.def(boost::python::init<>());
    muttable_double_wrapper.def_readwrite("value", &MuttableDouble::value, "value");

    boost::python::def("foo", foo_wrapper, "a function which take a pointer");
}
