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
#include "tools/tools.h"

#include <cmath>
#include <iostream>

const static double PI = std::acos(-1);

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

double simulator::SinusoidalSignal::computeSignalValue(double time) const {
    double signal_value = this->amplitude * std::sin(2.0 * PI * this->frequency * time + this->phase);
}

void simulator::SinusoidalSignal::updateActuators() {
    // TODO !!!

    /*
     * GET PERCEPTS
     */

    double simulation_duration_sec;

    if(this->sensorSet.size() != 1) {
       throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Clock\" sensor."); 
    }

    std::set<simulator::Sensor *>::iterator sensor_it;

    for(sensor_it = this->sensorSet.begin() ; sensor_it != this->sensorSet.end() ; sensor_it++) {
        if(simulator::Clock * clock_sensor = dynamic_cast<simulator::Clock *>(*sensor_it)) {
            Eigen::VectorXd percept_vector = (*sensor_it)->getPercepts();

            simulation_duration_sec = percept_vector[0];  // TODO !!!
        } else {
            throw std::invalid_argument("The \"sinusoid controller\" must have exactly one \"Clock\" sensor."); 
        }
    }

    //double signal_value = this->amplitude * std::sin(2.0 * PI * this->frequency * simulation_duration_sec + this->phase);
    double signal_value = this->computeSignalValue(simulation_duration_sec);

    std::cout << simulation_duration_sec << " : " << signal_value << std::endl;

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

