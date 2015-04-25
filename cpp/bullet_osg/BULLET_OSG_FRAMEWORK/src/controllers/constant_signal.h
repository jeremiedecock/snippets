/* 
 * Bullet OSG Framework.
 * The constant signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_CONSTANT_SIGNAL_CONTROLLER_H
#define BOTSIM_CONSTANT_SIGNAL_CONTROLLER_H

#include "controller.h"

namespace simulator {

    class ConstantSignal: public simulator::Controller {
        protected:
            // Common
            double constantValue; // The value of the signal.
            std::string name;     // The name of this instance.

        public:
            ConstantSignal(std::set<simulator::Actuator *> actuator_set,
                           std::set<simulator::Sensor *> sensor_set,
                           double _constant_value,
                           std::string _name="");

            ~ConstantSignal();

            void updateActuators();

            double getConstantValue() const;

            std::string getName() const;
    };

}

#endif // BOTSIM_CONSTANT_SIGNAL_CONTROLLER_H
