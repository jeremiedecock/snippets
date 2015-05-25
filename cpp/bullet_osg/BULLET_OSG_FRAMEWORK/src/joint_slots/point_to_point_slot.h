/* 
 * Bullet OSG Framework.
 * The point to point slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_POINT_TO_POINT_SLOT_H
#define BOTSIM_POINT_TO_POINT_SLOT_H

#include "joint_slot.h"

#include <Eigen/Dense>

namespace simulator {

    class PointToPointSlot: public simulator::JointSlot {

        protected:
            Eigen::Vector3d pivot;

        public:
            PointToPointSlot(Eigen::Vector3d pivot);

            virtual ~PointToPointSlot();

            Eigen::Vector3d getPivot() const;

        private:
            /**
             * Forbid copy of instances.
             */
            PointToPointSlot(const PointToPointSlot &);

            /**
             * Forbid assignment.
             */
            PointToPointSlot & operator = (const PointToPointSlot &);
    };

}

#endif // BOTSIM_POINT_TO_POINT_SLOT_H
