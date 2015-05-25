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

namespace botsim {

    class Fixed: public botsim::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Fixed(botsim::Part * part1,
                  botsim::Part * part2,
                  botsim::FixedSlot * joint_slot_for_part1,
                  botsim::FixedSlot * joint_slot_for_part2,
                  std::string _name="");

            Fixed(botsim::Part * part,
                  botsim::FixedSlot * joint_slot,
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
