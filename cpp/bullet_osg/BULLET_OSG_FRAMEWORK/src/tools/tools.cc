/* 
 * Bullet OSG Framework.
 * Tools module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "tools.h"

#include <cstdio>

btVector3 simulator::vec3_eigen_to_bullet(const Eigen::Vector3d &eigen_vector) {
    btVector3 bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2));
    return bt_vector;
}


btQuaternion simulator::vec4_eigen_to_bullet(const Eigen::Vector4d &eigen_vector) {
    btQuaternion bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2), eigen_vector(3));
    return bt_vector;
}


Eigen::Vector3d simulator::vec3_bullet_to_eigen(const btVector3 &bt_vector) {
    Eigen::Vector3d eigen_vector(bt_vector[0], bt_vector[1], bt_vector[2]);
    return eigen_vector;
}


Eigen::Vector4d simulator::vec4_bullet_to_eigen(const btVector4 &bt_vector) {
    Eigen::Vector4d eigen_vector(bt_vector[0], bt_vector[1], bt_vector[2], bt_vector[3]);
    return eigen_vector;
}


std::string simulator::eigen_vector_to_string(const Eigen::VectorXd &eigen_vector, std::string separator) {
    std::ostringstream oss;

    for(unsigned int i=0 ; i < eigen_vector.size() ; i++) {
        oss << eigen_vector[i];
        if((i + 1) < eigen_vector.size()) {
            oss << separator;
        }
    }

    return oss.str();
}


bool simulator::file_exists(const char * filename) {
    if(FILE * file = fopen(filename, "r")) {
        fclose(file);
        return true;
    }
    return false;
}

