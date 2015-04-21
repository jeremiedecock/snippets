/* 
 * Bullet OSG Framework.
 * Object module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef OBJECT_H
#define OBJECT_H

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

        public:
            Object(std::set<simulator::Part *> part_set,
                   std::set<simulator::Joint *> joint_set,
                   std::string _name="");

            std::set<simulator::Part *> getPartSet() const;

            std::set<simulator::Joint *> getJointSet() const;

            std::string getName() const;
    };

}

#endif // OBJECT_H
