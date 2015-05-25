/* 
 * Bullet OSG Framework.
 * Joint module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "joint.h"

btTypedConstraint * botsim::Joint::getBulletTypedConstraint() const {
    return this->bulletTypedConstraint;
}

