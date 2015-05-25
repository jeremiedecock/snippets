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

botsim::PointToPoint::PointToPoint(botsim::Part * part1,
                                      botsim::Part * part2,
                                      botsim::PointToPointSlot * joint_slot_for_part1,
                                      botsim::PointToPointSlot * joint_slot_for_part2,
                                      std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body1 = part1->getRigidBody();
    btRigidBody * bt_rigid_body2 = part2->getRigidBody();

    Eigen::Vector3d pivot_in_part1 = joint_slot_for_part1->getPivot();
    Eigen::Vector3d pivot_in_part2 = joint_slot_for_part2->getPivot();
    btVector3 bt_pivot_in_part1 = botsim::vec3_eigen_to_bullet(pivot_in_part1);
    btVector3 bt_pivot_in_part2 = botsim::vec3_eigen_to_bullet(pivot_in_part2);

    this->bulletTypedConstraint = new btPoint2PointConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2);
}

botsim::PointToPoint::PointToPoint(botsim::Part * part,
                                      botsim::PointToPointSlot * joint_slot,
                                      std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body = part->getRigidBody();

    Eigen::Vector3d pivot = joint_slot->getPivot();
    btVector3 bt_pivot_in_part = botsim::vec3_eigen_to_bullet(pivot);

    this->bulletTypedConstraint = new btPoint2PointConstraint(*bt_rigid_body, bt_pivot_in_part);
}

botsim::PointToPoint::~PointToPoint() {
    delete this->bulletTypedConstraint;
}

std::string botsim::PointToPoint::getName() const {
    return this->name;
}

