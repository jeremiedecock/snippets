/* 
 * Bullet OSG Framework.
 * Tools module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_TOOLS_H
#define BOTSIM_TOOLS_H

#include <boost/algorithm/string.hpp>
#include <boost/foreach.hpp>
#include <boost/lexical_cast.hpp>

#include <btBulletDynamicsCommon.h>
#include <Eigen/Dense>

namespace simulator {

    /**
     *
     */
    inline btVector3 vec3_eigen_to_bullet(const Eigen::Vector3d &eigen_vector) {
        btVector3 bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2));
        return bt_vector;
    }


    /**
     *
     */
    inline btQuaternion vec4_eigen_to_bullet(const Eigen::Vector4d &eigen_vector) {
        btQuaternion bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2), eigen_vector(3));
        return bt_vector;
    }


    /**
     *
     */
    inline Eigen::Vector3d vec3_bullet_to_eigen(const btVector3 &bt_vector) {
        Eigen::Vector3d eigen_vector(bt_vector[0], bt_vector[1], bt_vector[2]);
        return eigen_vector;
    }


    /**
     *
     */
    inline Eigen::Vector4d vec4_bullet_to_eigen(const btQuaternion &bt_vector) {
        Eigen::Vector4d eigen_vector(bt_vector[0], bt_vector[1], bt_vector[2], bt_vector[3]);
        return eigen_vector;
    }


    /**
     * Build a std::vector form a std::string
     */
    template <class T> std::vector<T> string_to_std_vector(const std::string &string_vector, std::string separator = ",") {

        // Split the std::string : build a std::vector of std::string
        std::vector<std::string> vector_of_strings;
        boost::split(vector_of_strings, string_vector, boost::is_any_of(separator.c_str()));

        // Build a std::vector of T (number, ...)
        std::vector<T> v;
        BOOST_FOREACH(std::string element_string, vector_of_strings) {
            try {
                v.push_back(boost::lexical_cast<T>(element_string));
            } catch (boost::bad_lexical_cast &) {
                std::cerr << "ERROR : wrong format for " << string_vector << " option !"
                    << std::endl;
            }
        }

        return v;
    }


    /**
     * Get a std::string representation of an eigen vector.
     */
    std::string eigen_vector_to_string(const Eigen::VectorXd &eigen_vector, std::string separator = ",");


    /**
     * Build an Eigen vector form a std::string
     */
    Eigen::Vector2d string_to_eigen_vector2(const std::string & string_vector);

    /**
     * Build an Eigen vector form a std::string
     */
    Eigen::Vector3d string_to_eigen_vector3(const std::string & string_vector);

    /**
     * Build an Eigen vector form a std::string
     */
    Eigen::Vector4d string_to_eigen_vector4(const std::string & string_vector);


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

}

#endif // BOTSIM_TOOLS_H
