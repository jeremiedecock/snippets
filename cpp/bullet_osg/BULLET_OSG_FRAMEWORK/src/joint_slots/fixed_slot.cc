/* 
 * Bullet OSG Framework.
 * The fixed slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "fixed_slot.h"

simulator::FixedSlot::FixedSlot(Eigen::Vector3d _pivot) : pivot(_pivot) {

}

simulator::FixedSlot::~FixedSlot() {
    // TODO
}

Eigen::Vector3d simulator::FixedSlot::getPivot() const {
    return this->pivot;
}

