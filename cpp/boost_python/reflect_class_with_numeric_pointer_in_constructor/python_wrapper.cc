#include <boost/python.hpp>
#include "classes.h"

// Fix muttable issue...

class MuttableDouble {
    public:
    double value;

    public:
    MuttableDouble() {};
    MuttableDouble(double x) : value(x) {};
};

// Workaround for MuttableDouble

class FooWrapper : public Foo {
    public:
    FooWrapper(MuttableDouble * muttable_x) : Foo(&(muttable_x->value)) { }
};

// Define python module

BOOST_PYTHON_MODULE(cppclasses)
{
    // MuttableDouble class
    boost::python::class_<MuttableDouble> muttable_double_wrapper("MuttableDouble", boost::python::init<double>());
    muttable_double_wrapper.def(boost::python::init<>());
    muttable_double_wrapper.def_readwrite("value", &MuttableDouble::value, "value");

    // Foo class
    boost::python::class_<FooWrapper> foo_wrapper("Foo", boost::python::init<MuttableDouble *>());
    foo_wrapper.def("increment", &FooWrapper::incrementNum, "Increment num.");
}

