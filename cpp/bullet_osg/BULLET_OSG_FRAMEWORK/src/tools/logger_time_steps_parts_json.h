/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_LOGGER_TIME_STEPS_PARTS_JSON_H
#define BOTSIM_LOGGER_TIME_STEPS_PARTS_JSON_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace botsim {

    class LoggerTimeStepsPartsJson : public TimeStepObserver {
        private:
            std::string filepath;
            std::ofstream * ofs;
            std::set<botsim::Part *> observedPartSet;

            std::map<std::string, std::vector<double> > dataMap;

        public:
            LoggerTimeStepsPartsJson(std::set<botsim::Part *> observed_part_set, //=std::set<botsim::Part *>(),
                                     std::string filepath="");

            ~LoggerTimeStepsPartsJson();

            void update(BulletEnvironment * bullet_environment);

            std::string getFilepath() const;

        private:
            /**
             * Forbid copy of instances.
             */
            LoggerTimeStepsPartsJson(const LoggerTimeStepsPartsJson &);

            /**
             * Forbid assignment.
             */
            LoggerTimeStepsPartsJson & operator = (const LoggerTimeStepsPartsJson &);
    };
}

#endif // BOTSIM_LOGGER_TIME_STEPS_PARTS_JSON_H
