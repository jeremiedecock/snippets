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

simulator::Clock::Clock(simulator::BulletEnvironment * bullet_environment,
                        std::string _name) :
                            bulletEnvironment(bullet_environment),
                            name(_name) {
    // TODO
}

simulator::Clock::~Clock() {
    // TODO
}

Eigen::VectorXd simulator::Clock::getPercepts() {
    const double simulation_duration_sec = this->bulletEnvironment->getElapsedSimulationTimeSecTickRes();
    //Eigen::VectorXd percept_vector(simulation_duration_sec);
    Eigen::VectorXd percept_vector = Eigen::VectorXd::Zero(1);  // TODO !
    percept_vector[0] = simulation_duration_sec;
    return percept_vector;
}

std::string simulator::Clock::getName() const {
    return this->name;
}

double simulator::Clock::getSimulationDurationSec() const {
    return this->simulationDurationSec;  // TODO: must be updated by the observed
}

