/* 
 * Bullet OSG Framework.
 * The fixed module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_FIXED_H
#define BOTSIM_FIXED_H

#include "joint.h"
#include "joint_slots/fixed_slot.h"
#include "part.h"

namespace simulator {

    class Fixed: public simulator::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Fixed(simulator::Part * part1,
                  simulator::Part * part2,
                  simulator::FixedSlot * joint_slot_for_part1,
                  simulator::FixedSlot * joint_slot_for_part2,
                  std::string _name="");

            Fixed(simulator::Part * part,
                  simulator::FixedSlot * joint_slot,
                  std::string _name="");

            ~Fixed();

            std::string getName() const;

        private:
            /**
             * Forbid copy of instances.
             */
            Fixed(const Fixed &);

            /**
             * Forbid assignment.
             */
            Fixed & operator = (const Fixed &);
    };

}

#endif // BOTSIM_FIXED_H
