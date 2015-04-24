/* 
 * Bullet OSG Framework.
 * The sinusoidal signal module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_SINUSOIDAL_SIGNAL_CONTROLLER_H
#define BOTSIM_SINUSOIDAL_SIGNAL_CONTROLLER_H

#include "controller.h"

namespace simulator {

    class SinusoidalSignal: public simulator::Controller {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            SinusoidalSignal(std::string _name="");

            ~SinusoidalSignal();

            std::string getName() const;
    };

}

#endif // BOTSIM_SINUSOIDAL_SIGNAL_CONTROLLER_H
