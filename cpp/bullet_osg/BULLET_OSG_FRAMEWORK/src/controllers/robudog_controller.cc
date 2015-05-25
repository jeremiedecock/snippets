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

botsim::RobudogController::RobudogController(std::set<botsim::Actuator *> actuator_set,
                                                std::set<botsim::Sensor *> sensor_set,
                                                Eigen::Matrix< double, 24, 1> _parameters,
                                                std::string _name) :
                                                  parameters(_parameters),
                                                  name(_name) {
    this->actuatorSet = actuator_set;
    this->sensorSet   = sensor_set;
}

botsim::RobudogController::~RobudogController() {
    // TODO
}

double botsim::RobudogController::computeSignalValue(double time, double amplitude, double frequency, double phase) const {
    double signal_value = amplitude * std::sin(2.0 * PI * frequency * time + phase);
}

void botsim::RobudogController::updateActuators() {

    /*
     * GET PERCEPTS
     */

    double simulation_duration_sec;

    if(this->sensorSet.size() != 1) {
       throw std::invalid_argument("The \"robudog controller\" must have exactly one \"Clock\" sensor."); 
    }

    std::set<botsim::Sensor *>::iterator sensor_it;

    for(sensor_it = this->sensorSet.begin() ; sensor_it != this->sensorSet.end() ; sensor_it++) {
        if(botsim::Clock * clock_sensor = dynamic_cast<botsim::Clock *>(*sensor_it)) {
            Eigen::VectorXd percept_vector = (*sensor_it)->getPercepts();

            simulation_duration_sec = percept_vector[0];  // TODO !!!
        } else {
            throw std::invalid_argument("The \"robudog controller\" must have exactly one \"Clock\" sensor."); 
        }
    }

    /*
     * UPDATE ACTUATORS
     */

    if(this->actuatorSet.size() != 8) {
        throw std::invalid_argument("The \"robudog controller\" must have exactly eight \"Motor\" actuator."); 
    }

    std::set<botsim::Actuator *>::iterator actuator_it;

    for(actuator_it = this->actuatorSet.begin() ; actuator_it != this->actuatorSet.end() ; actuator_it++) {
        if(botsim::Motor * motor_actuator = dynamic_cast<botsim::Motor *>(*actuator_it)) {
            int actuator_index;

            if(motor_actuator->getName() == "right_shoulder_motor") actuator_index = 0.;
            else if(motor_actuator->getName() == "left_shoulder_motor") actuator_index = 1.;
            else if(motor_actuator->getName() == "right_elbow_motor") actuator_index = 2.;
            else if(motor_actuator->getName() == "left_elbow_motor") actuator_index = 3.;
            else if(motor_actuator->getName() == "right_hip_motor") actuator_index = 4.;
            else if(motor_actuator->getName() == "left_hip_motor") actuator_index = 5.;
            else if(motor_actuator->getName() == "right_knee_motor") actuator_index = 6.;
            else if(motor_actuator->getName() == "left_knee_motor") actuator_index = 7.;
            else throw std::invalid_argument("Invalid motor name: " + motor_actuator->getName()); 

            double amplitude = this->parameters[actuator_index * 3];
            double frequency = this->parameters[actuator_index * 3 + 1];
            double phase =     this->parameters[actuator_index * 3 + 2];

            double signal_value = this->computeSignalValue(simulation_duration_sec, amplitude, frequency, phase);
            std::cout << simulation_duration_sec << " : " << motor_actuator->getName() << " = " <<  signal_value << std::endl;

            motor_actuator->setAngularVelocity(signal_value);
        } else {
            throw std::invalid_argument("The \"robudog controller\" must have exactly eight \"Motor\" actuator."); 
        }
    }
}

Eigen::Matrix< double, 24, 1> botsim::RobudogController::getParameters() const {
    return this->parameters;
}

std::string botsim::RobudogController::getName() const {
    return this->name;
}

