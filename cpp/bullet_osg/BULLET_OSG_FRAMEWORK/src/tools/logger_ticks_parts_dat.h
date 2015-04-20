/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef LOGGER_TICKS_PARTS_DAT_H
#define LOGGER_TICKS_PARTS_DAT_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>

namespace simulator {

    class LoggerTicksPartsDat : public BulletTickObserver {
        private:
            std::set<simulator::Part *> observedPartSet;

            std::map<std::string, std::ofstream *> fileMap;

        public:
            LoggerTicksPartsDat(std::set<simulator::Part *> observed_part_set);

            ~LoggerTicksPartsDat();

            void update(BulletEnvironment * bullet_environment);
    };
}

#endif // LOGGER_TICKS_PARTS_DAT_H
