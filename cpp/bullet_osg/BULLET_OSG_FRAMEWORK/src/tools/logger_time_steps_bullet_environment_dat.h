/* 
 * Bullet OSG Framework.
 * Bullet environment logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H
#define LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H

#include "bullet_environment.h"

#include <fstream>
#include <string>

namespace simulator {

    class LoggerTimeStepsBulletEnvironmentDat : public TimeStepObserver {
        private:
            std::string filepath;
            std::ofstream * ofs;

        public:
            LoggerTimeStepsBulletEnvironmentDat(std::string filepath="");

            ~LoggerTimeStepsBulletEnvironmentDat();

            void update(BulletEnvironment * bullet_environment);

            std::string getFilepath() const;
    };
}

#endif // LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H

