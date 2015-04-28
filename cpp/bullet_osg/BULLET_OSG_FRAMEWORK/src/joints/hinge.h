/* 
 * Bullet OSG Framework.
 * The hinge module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_HINGE_H
#define BOTSIM_HINGE_H

#include "joint.h"
#include "part.h"

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Hinge: public simulator::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            Hinge(simulator::Part * part1,
                  simulator::Part * part2,
                  Eigen::Vector3d pivot_in_part1,
                  Eigen::Vector3d pivot_in_part2,
                  Eigen::Vector3d axis_in_part1,
                  Eigen::Vector3d axis_in_part2,
                  std::string _name="");

            Hinge(simulator::Part * part,
                  Eigen::Vector3d pivot,
                  Eigen::Vector3d axis,
                  std::string _name="");

            virtual ~Hinge();

            std::string getName() const;
    };

}

#endif // BOTSIM_HINGE_H