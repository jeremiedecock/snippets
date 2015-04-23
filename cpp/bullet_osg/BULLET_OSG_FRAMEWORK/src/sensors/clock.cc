/* 
 * Bullet OSG Framework.
 * The clock module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "clock.h"

simulator::Clock::Clock(simulator::BulletEnvironment * bullet_environment,
                        std::string _name) {
    this->bulletEnvironment = bullet_environment;
    this->name = _name;
}

simulator::Clock::~Clock() {
    // TODO
}

std::string simulator::Clock::getName() const {
    return this->name;
}

