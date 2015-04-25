/* 
 * Bullet OSG Framework.
 * The constant signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "constant_signal.h"

#include <Eigen/Dense>

simulator::ConstantSignal::ConstantSignal(std::set<simulator::Actuator *> actuator_set,
                                          std::set<simulator::Sensor *> sensor_set,
                                          double _const_value,
                                          std::string _name) :
                                            constantValue(_const_value),
                                            name(_name) {
    this->actuatorSet = actuator_set;
    this->sensorSet   = sensor_set;
}

simulator::ConstantSignal::~ConstantSignal() {
    // TODO
}

void simulator::ConstantSignal::updateActuators() {
    // TODO !!!
    std::set<simulator::Actuator *>::iterator actuator_it;

    for(actuator_it = this->actuatorSet.begin() ; actuator_it != this->actuatorSet.end() ; actuator_it++) {
        //(*actuator_it)->...(this->constantValue);
    }
}

double simulator::ConstantSignal::getConstantValue() const {
    return this->constantValue;
}

std::string simulator::ConstantSignal::getName() const {
    return this->name;
}

