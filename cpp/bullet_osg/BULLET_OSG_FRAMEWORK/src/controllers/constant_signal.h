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
            std::string name;                         // the name of this instance

        public:
            ConstantSignal(std::string _name="");

            ~ConstantSignal();

            std::string getName() const;
    };

}

#endif // BOTSIM_CONSTANT_SIGNAL_CONTROLLER_H
