/* 
 * Bullet OSG Framework.
 * Actuator module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_ACTUATOR_H
#define BOTSIM_ACTUATOR_H

#include "joint.h"

namespace simulator {

    class Actuator: public simulator::Joint {
        public:
            virtual ~Actuator() {};
    };

}

#endif // BOTSIM_ACTUATOR_H
