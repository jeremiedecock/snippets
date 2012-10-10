#include <boost/python.hpp>
#include "classes.h"

class HelloWrapper : public Hello, public boost::python::wrapper<Hello>
{
    public:
        void message() {
            if(boost::python::override message = this->get_override("message")) {
                // WARNING: here, message() doesn't return anything, so the wrapper neither.
                //          If message() had returned something, we would have written:
                //          "return message();"
                message();
            } else {
                // WARNING: here, message() doesn't return anything, so the wrapper neither.
                //          If message() had returned something, we would have written:
                //          "return Hello::message();"
                Hello::message();
            }
        }

        void default_message() {
            // WARNING: here, message() doesn't return anything, so the wrapper neither.
            //          If message() had returned something, we would have written:
            //          "return this->Hello::message();"
            this->Hello::message();
        }
};

BOOST_PYTHON_MODULE(cppclasses)
{
    boost::python::class_<HelloWrapper, boost::noncopyable> hello_wrapper("Hello");
    hello_wrapper.def("message", &Hello::message, &HelloWrapper::default_message, "Print a message.");
    hello_wrapper.def("get_name", &Hello::getName, "Get name.");
}
