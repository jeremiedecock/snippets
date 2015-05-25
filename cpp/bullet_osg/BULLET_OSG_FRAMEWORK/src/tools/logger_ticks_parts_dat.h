/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_LOGGER_TICKS_PARTS_DAT_H
#define BOTSIM_LOGGER_TICKS_PARTS_DAT_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>

namespace botsim {

    class LoggerTicksPartsDat : public BulletTickObserver {
        private:
            std::set<botsim::Part *> observedPartSet;

            std::map<std::string, std::ofstream *> fileMap;

        public:
            LoggerTicksPartsDat(std::set<botsim::Part *> observed_part_set);

            ~LoggerTicksPartsDat();

            void update(BulletEnvironment * bullet_environment);

        private:
            /**
             * Forbid copy of instances.
             */
            LoggerTicksPartsDat(const LoggerTicksPartsDat &);

            /**
             * Forbid assignment.
             */
            LoggerTicksPartsDat & operator = (const LoggerTicksPartsDat &);
    };
}

#endif // BOTSIM_LOGGER_TICKS_PARTS_DAT_H
