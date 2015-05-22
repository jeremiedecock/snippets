/* 
 * Bullet OSG Framework.
 * The fixed slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_FIXED_SLOT_H
#define BOTSIM_FIXED_SLOT_H

#include "joint_slot.h"

#include <Eigen/Dense>

namespace simulator {

    class FixedSlot: public simulator::JointSlot {

        protected:
            Eigen::Vector3d pivot;

        public:
            FixedSlot(Eigen::Vector3d pivot);

            virtual ~FixedSlot();

            Eigen::Vector3d getPivot() const;
    };

}

#endif // BOTSIM_FIXED_SLOT_H
