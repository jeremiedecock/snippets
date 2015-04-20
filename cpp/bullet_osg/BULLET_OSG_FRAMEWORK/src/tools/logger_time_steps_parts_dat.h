/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef LOGGER_TIME_STEPS_PARTS_DAT_H
#define LOGGER_TIME_STEPS_PARTS_DAT_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>

namespace simulator {

    class LoggerTimeStepsPartsDat : public TimeStepObserver {
        private:
            std::set<simulator::Part *> observedPartSet;

            std::map<std::string, std::ofstream *> fileMap;

        public:
            LoggerTimeStepsPartsDat(std::set<simulator::Part *> observed_part_set);

            ~LoggerTimeStepsPartsDat();

            void update(BulletEnvironment * bullet_environment);
    };
}

#endif // LOGGER_TIME_STEPS_PARTS_DAT_H
