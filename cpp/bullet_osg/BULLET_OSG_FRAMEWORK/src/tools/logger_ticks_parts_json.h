/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef LOGGER_TICKS_PARTS_JSON_H
#define LOGGER_TICKS_PARTS_JSON_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <map>
#include <set>
#include <string>
#include <vector>

namespace simulator {

    class LoggerTicksPartsJson : public BulletTickObserver {
        private:
            std::string filepath;
            std::ofstream * ofs;
            std::set<simulator::Part *> observedPartSet;

            std::map<std::string, std::vector<double> > dataMap;

        public:
            LoggerTicksPartsJson(std::set<simulator::Part *> observed_parts_set, //=std::set<simulator::Part *>(),
                          std::string filepath="");

            ~LoggerTicksPartsJson();

            void update(BulletEnvironment * bullet_environment);

            std::string getFilepath() const;
    };
}

#endif // LOGGER_TICKS_PARTS_JSON_H
