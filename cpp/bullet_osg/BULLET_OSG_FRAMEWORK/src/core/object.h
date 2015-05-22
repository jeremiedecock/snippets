/* 
 * Bullet OSG Framework.
 * Object module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_OBJECT_H
#define BOTSIM_OBJECT_H

#include "actuator.h"
#include "part.h"
#include "joint.h"

#include <set>
#include <string>

namespace simulator {

    class Object {
        private:
            std::string name;

        protected:
            std::set<simulator::Part *> partSet;

            std::set<simulator::Joint *> jointSet;

            std::set<simulator::Actuator *> actuatorSet;

        public:
            Object(std::set<simulator::Part *> part_set,
                   std::set<simulator::Joint *> joint_set,
                   std::set<simulator::Actuator *> actuator_set,
                   std::string _name="");

            std::set<simulator::Part *> getPartSet() const;

            std::set<simulator::Joint *> getJointSet() const;

            std::set<simulator::Actuator *> getActuatorSet() const;

            std::string getName() const;

        private:
            /**
             * Forbid copy of instances.
             */
            Object(const Object &);

            /**
             * Forbid assignment.
             */
            Object & operator = (const Object &);
    };

}

#endif // BOTSIM_OBJECT_H
