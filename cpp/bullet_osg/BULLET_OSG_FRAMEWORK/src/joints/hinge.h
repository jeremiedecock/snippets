/* 
 * Bullet OSG Framework.
 * The hinge module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_HINGE_H
#define BOTSIM_HINGE_H

#include "joint.h"
#include "joint_slots/hinge_slot.h"
#include "part.h"

namespace botsim {

    class Hinge: public botsim::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Hinge(botsim::Part * part1,
                  botsim::Part * part2,
                  botsim::HingeSlot * joint_slot_for_part1,
                  botsim::HingeSlot * joint_slot_for_part2,
                  std::string _name="");

            Hinge(botsim::Part * part,
                  botsim::HingeSlot * joint_slot,
                  std::string _name="");

            virtual ~Hinge();

            std::string getName() const;

        private:
            /**
             * Forbid copy of instances.
             */
            Hinge(const Hinge &);

            /**
             * Forbid assignment.
             */
            Hinge & operator = (const Hinge &);
    };

}

#endif // BOTSIM_HINGE_H
