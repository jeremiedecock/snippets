/* 
 * Bullet OSG Framework.
 * Robudog JD module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_ROBUDOG_JD_H
#define BOTSIM_ROBUDOG_JD_H

#include "object.h"

namespace botsim {

    botsim::Object * make_robudog_jd(const Eigen::Vector3d object_initial_position, std::string object_name);

}

#endif // BOTSIM_ROBUDOG_JD_H
