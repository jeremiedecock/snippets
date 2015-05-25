/* 
 * Bullet OSG Framework.
 * Dynamixel AX-12 module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_DYNAMIXEL_AX12_H
#define BOTSIM_DYNAMIXEL_AX12_H

#include "part.h"

namespace botsim {

    botsim::Part * make_dynamixel_ax12(const Eigen::Vector3d initial_position, const Eigen::Vector4d initial_angle, std::string name);

}

#endif // BOTSIM_DYNAMIXEL_AX12_H
