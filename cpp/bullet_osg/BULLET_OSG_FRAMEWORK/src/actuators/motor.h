/* 
 * Bullet OSG Framework.
 * The motor module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_MOTOR_H
#define BOTSIM_MOTOR_H

#include "actuator.h"
#include "joints/hinge.h"
#include "part.h"

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

#include <string>

namespace simulator {

    class Motor: public simulator::Actuator, public simulator::Hinge {
        public:
            Motor(simulator::Part * part1,
                  simulator::Part * part2,
                  Eigen::Vector3d pivot_in_part1,
                  Eigen::Vector3d pivot_in_part2,
                  Eigen::Vector3d axis_in_part1,
                  Eigen::Vector3d axis_in_part2,
                  std::string _name="");

            Motor(simulator::Part * part,
                  Eigen::Vector3d pivot,
                  Eigen::Vector3d axis,
                  std::string _name="");

            virtual ~Motor();
    };

}

#endif // BOTSIM_MOTOR_H
