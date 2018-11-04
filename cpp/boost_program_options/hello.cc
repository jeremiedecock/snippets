/* 
 * Chrono: measure time duration between two points with boost.datetime
 *
 * Copyright (c) 2012 Jérémie Decock
 *
 * Required: boost.program_options library
 * Usage: g++ hello.cc -lboost_program_options -o hello
 *
 */

#include <fstream>
#include <iostream>
#include <boost/program_options.hpp>

namespace po = boost::program_options;

int main(int argc, char ** argv) {

    /*
     * PARSE PROGRAM OPTIONS
     */

    /* *** Declare the supported options *** */

    po::options_description options_desc("Allowed options");
    options_desc.add_options()
        ("help", "produce help message")
        ("config", po::value<std::string>(), "set the config filename.")
        ("string_opt",  po::value<std::string>(), "a string option")
        ("integer_opt", po::value<int>(), "an integer option")
        ("double_opt",  po::value<double>(), "a float (double precision) option")
        ("boolean_opt", po::value<bool>(), "a boolean option")
    ;

    /* *** Parse commandline options *** */

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, options_desc), vm);

    /* *** Parse config file *** */

    std::string config_filename;

    if(vm.count("config")) {
        config_filename = vm["config"].as<std::string>();
    }

    std::ifstream ifs(config_filename.c_str());
    po::store(po::parse_config_file(ifs, options_desc), vm);
    ifs.close();

    /* *** Notify *** */

    po::notify(vm);    

    // Print help if required
    if(vm.count("help")) {
        std::cout << options_desc << std::endl;
        return 1;
    }

    /* *** Setup options *** */

    std::string string_var;
    int integer_var;
    double double_var;
    bool boolean_var;

    // Setup string_opt
    if(vm.count("string_opt")) {
        string_var = vm["string_opt"].as<std::string>();
        std::cout << "string option  = " << string_var << std::endl;
    }

    // Setup integer_opt
    if(vm.count("integer_opt")) {
        integer_var = vm["integer_opt"].as<int>();
        std::cout << "integer option = " << integer_var << std::endl;
    }

    // Setup double_opt
    if(vm.count("double_opt")) {
        double_var = vm["double_opt"].as<double>();
        std::cout << "double option  = " << double_var << std::endl;
    }

    // Setup boolean_opt
    if(vm.count("boolean_opt")) {
        boolean_var = vm["boolean_opt"].as<bool>();
        std::cout << "boolean option = " << boolean_var << std::endl;
    }

    /*
     * DO SOMETHING WITH PARSED OPTIONS...
     */

    // ...

}

