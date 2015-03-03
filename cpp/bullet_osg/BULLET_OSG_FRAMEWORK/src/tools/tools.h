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

#include <Eigen/Dense>
#include <btBulletDynamicsCommon.h>

namespace simulator {

    /**
     *
     */
    btVector3 vec3_eigen_to_bullet(const Eigen::Vector3d &eigen_vector);

    /**
     *
     */
    btQuaternion vec4_eigen_to_bullet(const Eigen::Vector4d &eigen_vector);

}

#endif // TOOLS_H
