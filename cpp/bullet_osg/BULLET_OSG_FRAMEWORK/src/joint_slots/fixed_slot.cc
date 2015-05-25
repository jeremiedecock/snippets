/* 
 * Bullet OSG Framework.
 * The fixed slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "fixed_slot.h"

botsim::FixedSlot::FixedSlot(Eigen::Vector3d _pivot) : pivot(_pivot) {

}

botsim::FixedSlot::~FixedSlot() {
    // TODO
}

Eigen::Vector3d botsim::FixedSlot::getPivot() const {
    return this->pivot;
}

