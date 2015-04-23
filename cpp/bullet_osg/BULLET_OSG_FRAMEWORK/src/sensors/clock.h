/* 
 * Bullet OSG Framework.
 * The clock module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_CLOCK_SENSOR_H
#define BOTSIM_CLOCK_SENSOR_H

#include "bullet_environment.h"
#include "sensor.h"

namespace simulator {

    class Clock: public simulator::Sensor {
        protected:
            // Common
            std::string name;                         // the name of this instance

            simulator::BulletEnvironment * bulletEnvironment;

        public:
            Clock(simulator::BulletEnvironment * bullet_environment,
                  std::string _name="");

            ~Clock();

            std::string getName() const;
    };

}

#endif // BOTSIM_CLOCK_SENSOR_H
