/* 
 * Bullet OSG Framework.
 * Tools module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef TOOLS_H
#define TOOLS_H

//#include <boost/foreach.hpp>
//#include <boost/lexical_cast.hpp>
#include <btBulletDynamicsCommon.h>
#include <Eigen/Dense>

namespace simulator {

    /**
     *
     */
    btVector3 vec3_eigen_to_bullet(const Eigen::Vector3d &eigen_vector);

    /**
     *
     */
    btQuaternion vec4_eigen_to_bullet(const Eigen::Vector4d &eigen_vector);

    /**
     * Get a std::string representation of an eigen vector.
     */
    std::string eigen_vector_to_string(const Eigen::VectorXd &eigen_vector, std::string separator = ",");

    /**
     *
     */
    bool file_exists(const char *);

    /**
     * Convert any variable to a std::string.
     */
    template <class T> std::string to_string(const T &t) {
        std::ostringstream oss;
        oss << t;
        return oss.str();
    }

    /**
     * Convert any variable to a std::string.
     */
    template <class T> std::string to_string(const T &t, int precision) {
        std::ostringstream oss;
        oss.precision(precision);
        oss << std::fixed;
        oss << t;
        return oss.str();
    }

    /**
     * Get a std::string representation of a std::vector
     */
    template <class T> std::string vector_to_string(const std::vector<T> &v, std::string separator = ",") {
        std::ostringstream oss;

        for(unsigned i = 0; i < v.size(); i++) {
            oss << v[i];
            if((i + 1) < v.size()) {
                oss << separator;
            }
        }

        return oss.str();
    }

    /**
     * Get a std::string representation of a std::vector
     */
    template <class T> std::string nested_vector_to_string(const std::vector<T> &v, std::string separator1 = "\n", std::string separator2 = ",") {
        std::ostringstream oss;

        for(int i = 0; i < (int)v.size(); i++) {
            oss << vector_to_string(v[i], separator2);
            if((i + 1) < v.size()) {
                oss << separator1;
            }
        }

        return oss.str();
    }

//    /**
//     * Build a std::vector form a std::string
//     */
//    template <class T> std::vector<T> string_to_vector(const std::string &str, std::string separator = ",") {
//
//        // Split the std::string : build a std::vector of std::string
//        std::vector<std::string> string_vector;
//        boost::split(string_vector, str, boost::is_any_of(separator.c_str()));
//
//        // Build a std::vector of T (number, ...)
//        std::vector<T> v;
//        BOOST_FOREACH (std::string element_string, string_vector) {
//            try {
//                v.push_back(boost::lexical_cast<T>(element_string));
//            } catch (boost::bad_lexical_cast &) {
//                std::cerr << "ERROR : wrong format for " << str << " option !"
//                    << std::endl;
//            }
//        }
//
//        return v;
//    }

}

#endif // TOOLS_H
