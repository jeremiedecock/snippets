/* 
 * Bullet OSG Framework.
 * Object module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "object.h"

simulator::Object::Object(std::set<simulator::Part *> part_set,
                          std::string _name) :
                              partSet(part_set),
                              name(_name) {
    // TODO
}

std::set<simulator::Part *> simulator::Object::getPartSet() const {
    return this->partSet;
}

std::string simulator::Object::getName() const {
    return this->name;
}
