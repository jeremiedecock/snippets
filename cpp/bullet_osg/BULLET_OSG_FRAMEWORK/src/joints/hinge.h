/* 
 * Bullet OSG Framework.
 * The hinge module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef HINGE_H
#define HINGE_H

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
                  std::string name="");

            ~Hinge();

            std::string getName() const;
    };

}

#endif // HINGE_H
