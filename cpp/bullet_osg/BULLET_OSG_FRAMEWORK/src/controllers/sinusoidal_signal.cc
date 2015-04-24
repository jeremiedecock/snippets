/* 
 * Bullet OSG Framework.
 * The sinusoidal signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "sinusoidal_signal.h"

simulator::SinusoidalSignal::SinusoidalSignal(std::string _name) {
    this->name = _name;
}

simulator::SinusoidalSignal::~SinusoidalSignal() {
    // TODO
}

std::string simulator::SinusoidalSignal::getName() const {
    return this->name;
}

