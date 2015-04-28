/* 
 * Bullet OSG Framework.
 * The constant signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "constant_signal.h"

#include "actuators/motor.h"

#include <Eigen/Dense>

#include <iostream>

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

    double signal_value = this->constantValue;
    std::cout << signal_value << std::endl;

    /*
     * UPDATE ACTUATORS
     */

    if(this->actuatorSet.size() != 1) {
        throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Motor\" actuator."); 
    }

    std::set<simulator::Actuator *>::iterator actuator_it;

    for(actuator_it = this->actuatorSet.begin() ; actuator_it != this->actuatorSet.end() ; actuator_it++) {
        if(simulator::Motor * motor_actuator = dynamic_cast<simulator::Motor *>(*actuator_it)) {
            motor_actuator->setAngularVelocity(signal_value);
        } else {
            throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Motor\" actuator."); 
        }
    }
}

double simulator::ConstantSignal::getConstantValue() const {
    return this->constantValue;
}

std::string simulator::ConstantSignal::getName() const {
    return this->name;
}

