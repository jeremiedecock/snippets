/*
 * Copyright (c) 2014 Jérémie DECOCK (http://www.jdhp.org)
 */

#ifndef UTILS_H
#define UTILS_H

#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include <boost/algorithm/string.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast.hpp>

#ifdef EXEC_VERBOSE
#define PRINT(X) std::cout << "- " << #X << " : " << (X) << std::endl
#define PRINT_VEC(X) std::cout << "- " << #X << " : " << (vector_to_string(X)) << std::endl
#define PRINT_VEC_VEC(X) std::cout << "- " << #X << " : " << std::endl << (nested_vector_to_string(X)) << std::endl
#else
#define PRINT(X) 
#define PRINT_VEC(X)
#define PRINT_VEC_VEC(X)
#endif

/**
 * Return the mean value for a vector of double.
 */
double average_value(const std::vector<double> & v);

/**
 * Return the standard deviation for a vector of double.
 */
double standard_deviation(const std::vector<double> & v);

/**
 * Express a value in percent.
 */
double expressed_in_percent(const double & value_to_express, const double & reference_value);

/**
 * Convert any variable to a string.
 */
template <class T>
std::string to_string(const T & t)
{
    std::ostringstream oss;
    oss << t;
    return oss.str();
}

/**
 * Convert any variable to a string.
 */
template <class T>
std::string to_string(const T & t, int precision)
{
    std::ostringstream oss;
    oss.precision(precision);
    oss << std::fixed;
    oss << t;
    return oss.str();
}

/**
 * Get a string representation of a vector
 */
template <class T>
std::string vector_to_string(const std::vector<T>& v, std::string separator=",")
{
    std::ostringstream oss;

    for(int i = 0 ; i < (int)v.size() ; i++) {
        oss << v[i];
        if((i + 1) < v.size()) {
            oss << separator;
        }
    }

    return oss.str();
}

/**
 * Get a string representation of a vector
 */
template <class T>
std::string nested_vector_to_string(const std::vector<T>& v, std::string separator1="\n", std::string separator2=",")
{
    std::ostringstream oss;

    for(int i = 0 ; i < (int)v.size() ; i++) {
        oss << vector_to_string(v[i], separator2);
        if((i + 1) < v.size()) {
            oss << separator1;
        }
    }

    return oss.str();
}

/**
 * Build a vector form a string
 */
template <class T>
std::vector<T> string_to_vector(const std::string & str, std::string separator = ",")
{

    // Split the string : build a vector of string
    std::vector<std::string> string_vector;
    boost::split(string_vector, str, boost::is_any_of(separator.c_str()));

    // Build a vector of T (number, ...)
    std::vector<T> v;
    BOOST_FOREACH(std::string element_string, string_vector) {
        try {
            v.push_back(boost::lexical_cast<T>(element_string));
        } catch(boost::bad_lexical_cast &) {
            std::cerr << "ERROR : wrong format for " << str << " option !" << std::endl;
        }
    }

    return v;
}

/**
 *
 */
inline void basic_meter()
{
    static int function_call_number = 0;
    function_call_number++;
    std::cout << function_call_number << " ";
}

#endif //UTILS_H
