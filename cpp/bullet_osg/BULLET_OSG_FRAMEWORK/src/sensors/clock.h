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

#include <Eigen/Dense>

namespace simulator {

    class Clock: public simulator::Sensor {
        protected:
            // Common
            //simulator::BulletEnvironment * bulletEnvironment;

            std::string name;                         // the name of this instance

        public:
            simulator::BulletEnvironment * bulletEnvironment;  // TODO: UGLY WORKAROUND !

        public:
            Clock(simulator::BulletEnvironment * bullet_environment,
                  std::string _name="");

            ~Clock();

            Eigen::VectorXd getPercepts();

            std::string getName() const;
    };

}

#endif // BOTSIM_CLOCK_SENSOR_H
