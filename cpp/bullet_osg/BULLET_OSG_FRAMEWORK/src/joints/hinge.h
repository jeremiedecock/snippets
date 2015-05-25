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

namespace simulator {

    class Hinge: public simulator::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Hinge(simulator::Part * part1,
                  simulator::Part * part2,
                  simulator::HingeSlot * joint_slot_for_part1,
                  simulator::HingeSlot * joint_slot_for_part2,
                  std::string _name="");

            Hinge(simulator::Part * part,
                  simulator::HingeSlot * joint_slot,
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
