/* 
 * Bullet OSG Framework.
 * Sensor module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_SENSOR_H
#define BOTSIM_SENSOR_H

#include <Eigen/Dense>

#include <string>

namespace simulator {

    class Sensor {
        public:
            virtual ~Sensor() {};

            virtual Eigen::VectorXd getPercepts() = 0;

            virtual std::string getName() const = 0;

        protected:
            /**
             * Forbid instantiation.
             */
            Sensor() {};   // TODO ?

        private:
            /**
             * Forbid copy of instances.
             */
            Sensor(const Sensor &);

            /**
             * Forbid assignment.
             */
            Sensor & operator = (const Sensor &);
    };

}

#endif // BOTSIM_SENSOR_H
