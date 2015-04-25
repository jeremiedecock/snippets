/* 
 * Bullet OSG Framework.
 * Controller module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_CONTROLLER_H
#define BOTSIM_CONTROLLER_H

#include "actuator.h"
#include "sensor.h"

#include <set>
#include <string>

namespace simulator {

    class Controller {
        protected:
            std::set<simulator::Actuator *> actuatorSet;
            std::set<simulator::Sensor *> sensorSet;

        public:
            virtual ~Controller() {};

            virtual void updateActuators() = 0;
            
            std::set<simulator::Actuator *> getActuatorSet() const;

            std::set<simulator::Sensor *> getSensorSet() const;

            virtual std::string getName() const = 0;
    };

}

#endif // BOTSIM_CONTROLLER_H
