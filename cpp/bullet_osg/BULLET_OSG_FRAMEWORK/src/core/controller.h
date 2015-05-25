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

namespace botsim {

    class Controller {
        protected:
            std::set<botsim::Actuator *> actuatorSet;
            std::set<botsim::Sensor *> sensorSet;

        public:
            virtual ~Controller() {};

            virtual void updateActuators() = 0;
            
            std::set<botsim::Actuator *> getActuatorSet() const;

            std::set<botsim::Sensor *> getSensorSet() const;

            virtual std::string getName() const = 0;

        protected:
            /**
             * Forbid instantiation.
             */
            Controller() {};   // TODO ?

        private:
            /**
             * Forbid copy of instances.
             */
            Controller(const Controller &);

            /**
             * Forbid assignment.
             */
            Controller & operator = (const Controller &);
    };

}

#endif // BOTSIM_CONTROLLER_H
