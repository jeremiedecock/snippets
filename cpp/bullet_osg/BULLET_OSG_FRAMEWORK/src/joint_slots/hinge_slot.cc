/* 
 * Bullet OSG Framework.
 * The hinge slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "hinge_slot.h"

botsim::HingeSlot::HingeSlot(Eigen::Vector3d _pivot,
                                Eigen::Vector3d _axis) : 
                                    pivot(_pivot),
                                    axis(_axis) {
}

botsim::HingeSlot::~HingeSlot() {
    // TODO
}

Eigen::Vector3d botsim::HingeSlot::getPivot() const {
    return this->pivot;
}

Eigen::Vector3d botsim::HingeSlot::getAxis() const {
    return this->axis;
}

