#include <boost/python.hpp>
#include "functions.h"

BOOST_PYTHON_MODULE(cppfunctions)
{
    boost::python::class_<MuttableNumber> muttable_number_wrapper("MuttableNumber");
    muttable_number_wrapper.def_readwrite("value", &MuttableNumber::value, "value");

    boost::python::def("reference_wrong", reference_wrong, "a function which take a reference");
    boost::python::def("reference_right", reference_right, "a function which take a reference");
}
