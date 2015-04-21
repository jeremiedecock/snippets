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
                          std::set<simulator::Joint *> joint_set,
                          std::string _name) :
                              partSet(part_set),
                              jointSet(joint_set),
                              name(_name) {
    // TODO
}

std::set<simulator::Part *> simulator::Object::getPartSet() const {
    return this->partSet;
}

std::set<simulator::Joint *> simulator::Object::getJointSet() const {
    return this->jointSet;
}

std::string simulator::Object::getName() const {
    return this->name;
}
