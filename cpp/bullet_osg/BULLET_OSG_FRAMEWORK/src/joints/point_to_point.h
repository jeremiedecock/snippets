/* 
 * Bullet OSG Framework.
 * The point to point module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_POINT_TO_POINT_H
#define BOTSIM_POINT_TO_POINT_H

#include "joint.h"
#include "part.h"

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class PointToPoint: public simulator::Joint {
        protected:
            // Common
            std::string name;                         // the name of this instance

        public:
            PointToPoint(simulator::Part * part1,
                         simulator::Part * part2,
                         Eigen::Vector3d pivot_in_part1,
                         Eigen::Vector3d pivot_in_part2,
                         std::string _name="");

            PointToPoint(simulator::Part * part,
                         Eigen::Vector3d pivot,
                         std::string _name="");

            ~PointToPoint();

            std::string getName() const;
    };

}

#endif // BOTSIM_POINT_TO_POINT_H
