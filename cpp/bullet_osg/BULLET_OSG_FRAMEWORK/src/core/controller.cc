/* 
 * Bullet OSG Framework.
 * Controller module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "controller.h"

std::set<simulator::Actuator *> simulator::Controller::getActuatorSet() const {
    return this->actuatorSet;
}

std::set<simulator::Sensor *> simulator::Controller::getSensorSet() const {
    return this->sensorSet;
}
