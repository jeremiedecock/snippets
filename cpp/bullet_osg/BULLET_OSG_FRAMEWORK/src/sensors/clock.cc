/* 
 * Bullet OSG Framework.
 * The clock module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "clock.h"

#include "tools/tools.h"

#include <iostream>

botsim::Clock::Clock(botsim::BulletEnvironment * bullet_environment,
                        std::string _name) :
                            bulletEnvironment(bullet_environment),
                            name(_name) {
    // TODO
}

botsim::Clock::~Clock() {
    // TODO
}

Eigen::VectorXd botsim::Clock::getPercepts() {
    const double simulation_duration_sec = this->bulletEnvironment->getElapsedSimulationTimeSecTickRes();
    //Eigen::VectorXd percept_vector(simulation_duration_sec);
    Eigen::VectorXd percept_vector = Eigen::VectorXd::Zero(1);  // TODO !
    percept_vector[0] = simulation_duration_sec;
    return percept_vector;
}

std::string botsim::Clock::getName() const {
    return this->name;
}

double botsim::Clock::getSimulationDurationSec() const {
    return this->simulationDurationSec;  // TODO: must be updated by the observed
}

