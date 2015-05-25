/* 
 * Bullet OSG Framework.
 * Bullet environment logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H
#define BOTSIM_LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H

#include "bullet_environment.h"

#include <fstream>
#include <string>

namespace botsim {

    class LoggerTimeStepsBulletEnvironmentDat : public TimeStepObserver {
        private:
            std::string filepath;
            std::ofstream * ofs;

        public:
            LoggerTimeStepsBulletEnvironmentDat(std::string filepath="");

            ~LoggerTimeStepsBulletEnvironmentDat();

            void update(BulletEnvironment * bullet_environment);

            std::string getFilepath() const;

        private:
            /**
             * Forbid copy of instances.
             */
            LoggerTimeStepsBulletEnvironmentDat(const LoggerTimeStepsBulletEnvironmentDat &);

            /**
             * Forbid assignment.
             */
            LoggerTimeStepsBulletEnvironmentDat & operator = (const LoggerTimeStepsBulletEnvironmentDat &);
    };
}

#endif // BOTSIM_LOGGER_TIME_STEPS_BULLET_ENVIRONMENT_DAT_H
