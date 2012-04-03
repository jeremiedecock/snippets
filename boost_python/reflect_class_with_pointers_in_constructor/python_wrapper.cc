#include <boost/python.hpp>
#include "classes.h"

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<MuttableNumber> muttable_number_wrapper("MuttableNumber");
    muttable_number_wrapper.def_readwrite("value", &MuttableNumber::value, "value");

    boost::python::class_<Foo> foo_wrapper("Foo", boost::python::init<MuttableNumber *>());
    foo_wrapper.def("increment", &Foo::incrementNum, "Increment num.");
}
