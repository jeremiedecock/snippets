/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef PART_LOGGER_DAT_H
#define PART_LOGGER_DAT_H

#include "bullet_environment.h"
#include "part.h"

#include <fstream>
#include <set>
#include <string>

namespace simulator {

    class PartLoggerDat : public TimeStepObserver {
        private:
            std::string filepath;
            std::ofstream * ofs;
            std::set<simulator::Part *> observedPartSet;

        public:
            PartLoggerDat(std::set<simulator::Part *> observed_parts_set, //=std::set<simulator::Part *>(),
                          std::string filepath="");

            ~PartLoggerDat();

            void update(BulletEnvironment * bullet_environment);

            std::string getFilepath() const;
    };
}

#endif // PART_LOGGER_DAT_H
