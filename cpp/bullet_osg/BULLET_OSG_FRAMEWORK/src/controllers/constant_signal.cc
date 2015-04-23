/* 
 * Bullet OSG Framework.
 * The constant signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "constant_signal.h"

simulator::ConstantSignal::ConstantSignal(std::string _name) {
    this->name = _name;
}

simulator::ConstantSignal::~ConstantSignal() {
    // TODO
}

std::string simulator::ConstantSignal::getName() const {
    return this->name;
}

