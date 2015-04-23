/* 
 * Bullet OSG Framework.
 * The motor module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "motor.h"
#include "joints/hinge.h"

simulator::Motor::Motor(simulator::Part * part1,
                        simulator::Part * part2,
                        Eigen::Vector3d pivot_in_part1,
                        Eigen::Vector3d pivot_in_part2,
                        Eigen::Vector3d axis_in_part1,
                        Eigen::Vector3d axis_in_part2,
                        std::string _name) :
                            // call superclass (hinge) constructor
                            simulator::Hinge(part1, part2, pivot_in_part1, pivot_in_part2, axis_in_part1, axis_in_part2, _name) {
    // TODO ?
}

simulator::Motor::Motor(simulator::Part * part,
                        Eigen::Vector3d pivot,
                        Eigen::Vector3d axis,
                        std::string _name) :
                            // call superclass (hinge) constructor
                            simulator::Hinge(part, pivot, axis, _name) {
    // TODO ?
}

simulator::Motor::~Motor() {
    // TODO
}
