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

#include <string>

namespace simulator {

    class Controller {
        public:
            virtual ~Controller() {};

            // Misc
            
            virtual std::string getName() const = 0;
    };

}

#endif // BOTSIM_CONTROLLER_H
