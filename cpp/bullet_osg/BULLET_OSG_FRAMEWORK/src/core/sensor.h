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

#include <string>

namespace simulator {

    class Sensor {
        public:
            virtual ~Sensor() {};

            // Misc
            
            virtual std::string getName() const = 0;
    };

}

#endif // BOTSIM_SENSOR_H
