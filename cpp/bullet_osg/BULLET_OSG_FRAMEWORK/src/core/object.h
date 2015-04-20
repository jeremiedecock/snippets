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

#include <set>
#include <string>

namespace simulator {

    class Object {
        private:
            std::string name;

        protected:
            std::set<simulator::Part *> partSet;

        public:
            Object(std::set<simulator::Part *> part_set, std::string _name);

            std::set<simulator::Part *> getPartSet() const;

            std::string getName() const;
    };

}

#endif // OBJECT_H
