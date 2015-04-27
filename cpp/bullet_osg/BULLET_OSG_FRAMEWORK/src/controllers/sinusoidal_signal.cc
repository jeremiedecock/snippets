/* 
 * Bullet OSG Framework.
 * The sinusoidal signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "sinusoidal_signal.h"

#include "sensors/clock.h"

#include <iostream>

simulator::SinusoidalSignal::SinusoidalSignal(std::set<simulator::Actuator *> actuator_set,
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

simulator::SinusoidalSignal::~SinusoidalSignal() {
    // TODO
}

void simulator::SinusoidalSignal::updateActuators() {
    // TODO !!!

    /*
     * GET PERCEPTS
     */
    
    if(this->sensorSet.size() != 1) {
       throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Clock\" sensor."); 
    }

    std::set<simulator::Sensor *>::iterator sensor_it;

    for(sensor_it = this->sensorSet.begin() ; sensor_it != this->sensorSet.end() ; sensor_it++) {
        if(simulator::Clock * clock_sensor = dynamic_cast<simulator::Clock *>(*sensor_it)) {
            Eigen::VectorXd percept_vector = (*sensor_it)->getPercepts();

            double simulation_duration_sec = percept_vector[0];  // TODO !!!

            std::cout << simulation_duration_sec << std::endl;
        } else {
            throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Clock\" sensor."); 
        }
    }

    /*
     * UPDATE ACTUATORS
     */

    std::set<simulator::Actuator *>::iterator actuator_it;

    for(actuator_it = this->actuatorSet.begin() ; actuator_it != this->actuatorSet.end() ; actuator_it++) {
        //(*actuator_it)->...(this->constantValue);
    }
}

double simulator::SinusoidalSignal::getAmplitude() const {
    return this->amplitude;
}

double simulator::SinusoidalSignal::getFrequency() const {
    return this->frequency;
}

double simulator::SinusoidalSignal::getPhase() const {
    return this->phase;
}

std::string simulator::SinusoidalSignal::getName() const {
    return this->name;
}

