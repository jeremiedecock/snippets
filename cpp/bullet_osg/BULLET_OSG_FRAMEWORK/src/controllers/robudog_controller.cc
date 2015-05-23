/* 
 * Bullet OSG Framework.
 * The robudog controller module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "robudog_controller.h"

#include "actuators/motor.h"
#include "sensors/clock.h"
#include "tools/tools.h"

#include <cmath>
#include <iostream>

const static double PI = std::acos(-1);

simulator::RobudogController::RobudogController(std::set<simulator::Actuator *> actuator_set,
                                                std::set<simulator::Sensor *> sensor_set,
                                                double _amplitude,
                                                double _frequency,
                                                double _phase,
                                                std::string _name) :
                                                  amplitude(_amplitude),
                                                  frequency(_frequency),
                                                  phase(_phase),
                                                  name(_name) {
    this->actuatorSet = actuator_set;
    this->sensorSet   = sensor_set;
}

simulator::RobudogController::~RobudogController() {
    // TODO
}

double simulator::RobudogController::computeSignalValue(double time) const {
    double signal_value = this->amplitude * std::sin(2.0 * PI * this->frequency * time + this->phase);
}

void simulator::RobudogController::updateActuators() {

    /*
     * GET PERCEPTS
     */

    double simulation_duration_sec;

    if(this->sensorSet.size() != 1) {
       throw std::invalid_argument("The \"robudog controller\" must have exactly one \"Clock\" sensor."); 
    }

    std::set<simulator::Sensor *>::iterator sensor_it;

    for(sensor_it = this->sensorSet.begin() ; sensor_it != this->sensorSet.end() ; sensor_it++) {
        if(simulator::Clock * clock_sensor = dynamic_cast<simulator::Clock *>(*sensor_it)) {
            Eigen::VectorXd percept_vector = (*sensor_it)->getPercepts();

            simulation_duration_sec = percept_vector[0];  // TODO !!!
        } else {
            throw std::invalid_argument("The \"robudog controller\" must have exactly one \"Clock\" sensor."); 
        }
    }

    double signal_value = this->computeSignalValue(simulation_duration_sec);
    std::cout << simulation_duration_sec << " : " << signal_value << std::endl;

    /*
     * UPDATE ACTUATORS
     */

    if(this->actuatorSet.size() != 8) {
        throw std::invalid_argument("The \"robudog controller\" must have exactly eight \"Motor\" actuator."); 
    }

    std::set<simulator::Actuator *>::iterator actuator_it;

    for(actuator_it = this->actuatorSet.begin() ; actuator_it != this->actuatorSet.end() ; actuator_it++) {
        if(simulator::Motor * motor_actuator = dynamic_cast<simulator::Motor *>(*actuator_it)) {
            motor_actuator->setAngularVelocity(signal_value);
        } else {
            throw std::invalid_argument("The \"robudog controller\" must have exactly eight \"Motor\" actuator."); 
        }
    }
}

double simulator::RobudogController::getAmplitude() const {
    return this->amplitude;
}

double simulator::RobudogController::getFrequency() const {
    return this->frequency;
}

double simulator::RobudogController::getPhase() const {
    return this->phase;
}

std::string simulator::RobudogController::getName() const {
    return this->name;
}

