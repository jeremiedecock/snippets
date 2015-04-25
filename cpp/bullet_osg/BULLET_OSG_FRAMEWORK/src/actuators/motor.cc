/* 
 * Bullet OSG Framework.
 * The motor module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "motor.h"
//#include "joints/hinge.h"

#include "tools/tools.h"

simulator::Motor::Motor(simulator::Part * part1,
                        simulator::Part * part2,
                        Eigen::Vector3d pivot_in_part1,
                        Eigen::Vector3d pivot_in_part2,
                        Eigen::Vector3d axis_in_part1,
                        Eigen::Vector3d axis_in_part2,
                        std::string _name) //:
                            // call superclass (hinge) constructor
                            //simulator::Hinge(part1, part2, pivot_in_part1, pivot_in_part2, axis_in_part1, axis_in_part2, _name) {
                        {
    // TODO ?

    this->name = _name;

    btRigidBody * bt_rigid_body1 = part1->getRigidBody();
    btRigidBody * bt_rigid_body2 = part2->getRigidBody();
    btVector3 bt_pivot_in_part1 = simulator::vec3_eigen_to_bullet(pivot_in_part1);
    btVector3 bt_pivot_in_part2 = simulator::vec3_eigen_to_bullet(pivot_in_part2);
    btVector3 bt_axis_in_part1 = simulator::vec3_eigen_to_bullet(axis_in_part1);
    btVector3 bt_axis_in_part2 = simulator::vec3_eigen_to_bullet(axis_in_part2);

    this->bulletTypedConstraint = new btHingeConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2, bt_axis_in_part1, bt_axis_in_part2);
}

simulator::Motor::Motor(simulator::Part * part,
                        Eigen::Vector3d pivot,
                        Eigen::Vector3d axis,
                        std::string _name) //:
                            // call superclass (hinge) constructor
                            //simulator::Hinge(part, pivot, axis, _name) {
                            {
    // TODO ?

    this->name = _name;

    btRigidBody * bt_rigid_body = part->getRigidBody();
    btVector3 bt_pivot_in_part = simulator::vec3_eigen_to_bullet(pivot);
    btVector3 bt_axis_in_part = simulator::vec3_eigen_to_bullet(axis);

    this->bulletTypedConstraint = new btHingeConstraint(*bt_rigid_body, bt_pivot_in_part, bt_axis_in_part);
}

simulator::Motor::~Motor() {
    // TODO
}

std::string simulator::Motor::getName() const {
    return this->name;
}
