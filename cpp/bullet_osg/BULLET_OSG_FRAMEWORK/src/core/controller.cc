/* 
 * Bullet OSG Framework.
 * Controller module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "controller.h"

std::set<botsim::Actuator *> botsim::Controller::getActuatorSet() const {
    return this->actuatorSet;
}

std::set<botsim::Sensor *> botsim::Controller::getSensorSet() const {
    return this->sensorSet;
}
