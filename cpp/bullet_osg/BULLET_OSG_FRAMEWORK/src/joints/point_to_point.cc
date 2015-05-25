/* 
 * Bullet OSG Framework.
 * The point to point module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "point_to_point.h"

#include "tools/tools.h"

simulator::PointToPoint::PointToPoint(simulator::Part * part1,
                                      simulator::Part * part2,
                                      simulator::PointToPointSlot * joint_slot_for_part1,
                                      simulator::PointToPointSlot * joint_slot_for_part2,
                                      std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body1 = part1->getRigidBody();
    btRigidBody * bt_rigid_body2 = part2->getRigidBody();

    Eigen::Vector3d pivot_in_part1 = joint_slot_for_part1->getPivot();
    Eigen::Vector3d pivot_in_part2 = joint_slot_for_part2->getPivot();
    btVector3 bt_pivot_in_part1 = simulator::vec3_eigen_to_bullet(pivot_in_part1);
    btVector3 bt_pivot_in_part2 = simulator::vec3_eigen_to_bullet(pivot_in_part2);

    this->bulletTypedConstraint = new btPoint2PointConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2);
}

simulator::PointToPoint::PointToPoint(simulator::Part * part,
                                      simulator::PointToPointSlot * joint_slot,
                                      std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body = part->getRigidBody();

    Eigen::Vector3d pivot = joint_slot->getPivot();
    btVector3 bt_pivot_in_part = simulator::vec3_eigen_to_bullet(pivot);

    this->bulletTypedConstraint = new btPoint2PointConstraint(*bt_rigid_body, bt_pivot_in_part);
}

simulator::PointToPoint::~PointToPoint() {
    delete this->bulletTypedConstraint;
}

std::string simulator::PointToPoint::getName() const {
    return this->name;
}

