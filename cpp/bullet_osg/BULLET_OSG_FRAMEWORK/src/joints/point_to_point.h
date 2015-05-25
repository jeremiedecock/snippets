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

namespace botsim {

    class PointToPoint: public botsim::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            PointToPoint(botsim::Part * part1,
                         botsim::Part * part2,
                         botsim::PointToPointSlot * joint_slot_for_part1,
                         botsim::PointToPointSlot * joint_slot_for_part2,
                         std::string _name="");

            PointToPoint(botsim::Part * part,
                         botsim::PointToPointSlot * joint_slot,
                         std::string _name="");

            ~PointToPoint();

            std::string getName() const;

        private:
            /**
             * Forbid copy of instances.
             */
            PointToPoint(const PointToPoint &);

            /**
             * Forbid assignment.
             */
            PointToPoint & operator = (const PointToPoint &);
    };

}

#endif // BOTSIM_POINT_TO_POINT_H
