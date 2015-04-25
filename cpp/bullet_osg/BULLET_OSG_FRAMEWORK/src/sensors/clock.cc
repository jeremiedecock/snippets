/* 
 * Bullet OSG Framework.
 * The clock module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "clock.h"

simulator::Clock::Clock(//simulator::BulletEnvironment * bullet_environment,
                        std::string _name) :
                        //    bulletEnvironment(bullet_environment),
                            name(_name) {
    // TODO
}

simulator::Clock::~Clock() {
    // TODO
}

Eigen::VectorXd simulator::Clock::getPercepts() {
    //const double simulation_duration_sec = this->bulletEnvironment->getElapsedSimulationTimeSecTickRes();
    const double simulation_duration_sec = 0; // TODO !!!!!!!!!!!!!!
    Eigen::VectorXd percept_vector(simulation_duration_sec);
    return percept_vector;
}

std::string simulator::Clock::getName() const {
    return this->name;
}

