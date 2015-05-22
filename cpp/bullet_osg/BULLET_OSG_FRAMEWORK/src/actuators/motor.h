/* 
 * Bullet OSG Framework.
 * The motor module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_MOTOR_H
#define BOTSIM_MOTOR_H

#include "actuator.h"
#include "joints/hinge.h"
#include "joint_slots/hinge_slot.h"
#include "part.h"

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

#include <string>

namespace simulator {

    class Motor: public simulator::Actuator/*, public simulator::Hinge*/ { // TODO !!!
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Motor(simulator::Part * part1,
                  simulator::Part * part2,
                  simulator::HingeSlot * joint_slot_for_part1,
                  simulator::HingeSlot * joint_slot_for_part2,
                  std::string _name="");

            Motor(simulator::Part * part,
                  simulator::HingeSlot * joint_slot,
                  std::string _name="");

            virtual ~Motor();

            void setAngularVelocity(double target_velocity);

            std::string getName() const;

        private:
            /**
             * Forbid copy of instances.
             */
            Motor(const Motor &);

            /**
             * Forbid assignment.
             */
            Motor & operator = (const Motor &);
    };

}

#endif // BOTSIM_MOTOR_H
