/* 
 * Bullet OSG Framework.
 * Object module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "object.h"

botsim::Object::Object(std::set<botsim::Part *> part_set,
                          std::set<botsim::Joint *> joint_set,
                          std::set<botsim::Actuator *> actuator_set,
                          std::string _name) :
                              partSet(part_set),
                              jointSet(joint_set),
                              actuatorSet(actuator_set),
                              name(_name) {
    // TODO
}

std::set<botsim::Part *> botsim::Object::getPartSet() const {
    return this->partSet;
}

std::set<botsim::Joint *> botsim::Object::getJointSet() const {
    return this->jointSet;
}

std::set<botsim::Actuator *> botsim::Object::getActuatorSet() const {
    return this->actuatorSet;
}

std::string botsim::Object::getName() const {
    return this->name;
}
