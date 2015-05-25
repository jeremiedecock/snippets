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

namespace botsim {

    class Object {
        private:
            std::string name;

        protected:
            std::set<botsim::Part *> partSet;

            std::set<botsim::Joint *> jointSet;

            std::set<botsim::Actuator *> actuatorSet;

        public:
            Object(std::set<botsim::Part *> part_set,
                   std::set<botsim::Joint *> joint_set,
                   std::set<botsim::Actuator *> actuator_set,
                   std::string _name="");

            std::set<botsim::Part *> getPartSet() const;

            std::set<botsim::Joint *> getJointSet() const;

            std::set<botsim::Actuator *> getActuatorSet() const;

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
