#include <boost/python.hpp>
#include "functions.h"

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::class_<MuttableNumber> muttable_number_wrapper("MuttableNumber");
    muttable_number_wrapper.def_readwrite("value", &MuttableNumber::value, "value");

    boost::python::def("pointer_wrong", pointer_wrong, "a function which take a pointer");
    boost::python::def("pointer_right", pointer_right, "a function which take a pointer");
}
