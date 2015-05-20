/* 
 * Bullet OSG Framework.
 * The hinge slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "hinge_slot.h"

simulator::HingeSlot::HingeSlot(Eigen::Vector3d _pivot,
                                Eigen::Vector3d _axis) : 
                                    pivot(_pivot),
                                    axis(_axis) {
}

simulator::HingeSlot::~HingeSlot() {
    // TODO
}

Eigen::Vector3d simulator::HingeSlot::getPivot() const {
    return this->pivot;
}

Eigen::Vector3d simulator::HingeSlot::getAxis() const {
    return this->axis;
}

