/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_LOGGER_TIME_STEPS_PARTS_DAT_H
#define BOTSIM_LOGGER_TIME_STEPS_PARTS_DAT_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>

namespace botsim {

    class LoggerTimeStepsPartsDat : public TimeStepObserver {
        private:
            std::set<botsim::Part *> observedPartSet;

            std::map<std::string, std::ofstream *> fileMap;

        public:
            LoggerTimeStepsPartsDat(std::set<botsim::Part *> observed_part_set);

            ~LoggerTimeStepsPartsDat();

            void update(BulletEnvironment * bullet_environment);

        private:
            /**
             * Forbid copy of instances.
             */
            LoggerTimeStepsPartsDat(const LoggerTimeStepsPartsDat &);

            /**
             * Forbid assignment.
             */
            LoggerTimeStepsPartsDat & operator = (const LoggerTimeStepsPartsDat &);
    };
}

#endif // BOTSIM_LOGGER_TIME_STEPS_PARTS_DAT_H
