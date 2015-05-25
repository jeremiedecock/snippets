/* 
 * Bullet OSG Framework.
 * The point to point slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "point_to_point_slot.h"

botsim::PointToPointSlot::PointToPointSlot(Eigen::Vector3d _pivot) : pivot(_pivot) {

}

botsim::PointToPointSlot::~PointToPointSlot() {
    // TODO
}

Eigen::Vector3d botsim::PointToPointSlot::getPivot() const {
    return this->pivot;
}

