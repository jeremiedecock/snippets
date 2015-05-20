/* 
 * Bullet OSG Framework.
 * The point to point module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_POINT_TO_POINT_H
#define BOTSIM_POINT_TO_POINT_H

#include "joint.h"
#include "joint_slots/point_to_point_slot.h"
#include "part.h"

namespace simulator {

    class PointToPoint: public simulator::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            PointToPoint(simulator::Part * part1,
                         simulator::Part * part2,
                         simulator::PointToPointSlot * joint_slot_for_part1,
                         simulator::PointToPointSlot * joint_slot_for_part2,
                         std::string _name="");

            PointToPoint(simulator::Part * part,
                         simulator::PointToPointSlot * joint_slot,
                         std::string _name="");

            ~PointToPoint();

            std::string getName() const;
    };

}

#endif // BOTSIM_POINT_TO_POINT_H
