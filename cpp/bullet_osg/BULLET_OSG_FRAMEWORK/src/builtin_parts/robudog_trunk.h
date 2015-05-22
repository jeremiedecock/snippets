/* 
 * Bullet OSG Framework.
 * Robudog trunk module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_ROBUDOG_TRUNK_H
#define BOTSIM_ROBUDOG_TRUNK_H

#include "part.h"

namespace simulator {

    simulator::Part * make_robudog_trunk(const Eigen::Vector3d initial_position, const Eigen::Vector4d initial_angle, std::string name);

}

#endif // BOTSIM_ROBUDOG_TRUNK_H
