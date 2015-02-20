/* 
 * Bullet OSG Framework.
 * Tools module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "tools.h"

btVector3 simulator::vec3_eigen_to_bullet(const Eigen::Vector3d &eigen_vector) {
    btVector3 bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2));
    return bt_vector;
}

btQuaternion simulator::vec4_eigen_to_bullet(const Eigen::Vector4d &eigen_vector) {
    btQuaternion bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2), eigen_vector(3));
    return bt_vector;
}

