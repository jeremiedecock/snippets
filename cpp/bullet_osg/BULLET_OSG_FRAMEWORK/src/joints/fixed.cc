/* 
 * Bullet OSG Framework.
 * The fixed module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "fixed.h"

#include "tools/tools.h"

static const double low = 0.;
static const double high = 0.;
static const double softness = 0.9;
static const double bias_factor = 0.3;
static const double relaxation_factor = 1.0;

simulator::Fixed::Fixed(simulator::Part * part1,
                        simulator::Part * part2,
                        simulator::FixedSlot * joint_slot_for_part1,
                        simulator::FixedSlot * joint_slot_for_part2,
                        std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body1 = part1->getRigidBody();
    btRigidBody * bt_rigid_body2 = part2->getRigidBody();

    Eigen::Vector3d pivot_in_part1 = joint_slot_for_part1->getPivot();
    Eigen::Vector3d pivot_in_part2 = joint_slot_for_part2->getPivot();
    btVector3 bt_pivot_in_part1 = simulator::vec3_eigen_to_bullet(pivot_in_part1);
    btVector3 bt_pivot_in_part2 = simulator::vec3_eigen_to_bullet(pivot_in_part2);

    //this->bulletTypedConstraint = new btFixedConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2);
    btVector3 bt_axis_in_part1(0, 0, 1);
    btVector3 bt_axis_in_part2(0, 0, 1);
    btHingeConstraint * p_hinge_constraint = new btHingeConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2, bt_axis_in_part1, bt_axis_in_part2);
    p_hinge_constraint->setLimit(low, high, softness, bias_factor, relaxation_factor);
    this->bulletTypedConstraint = p_hinge_constraint;
}

simulator::Fixed::Fixed(simulator::Part * part,
                        simulator::FixedSlot * joint_slot,
                        std::string _name) {

    this->name = _name;

    btRigidBody * bt_rigid_body = part->getRigidBody();

    Eigen::Vector3d pivot = joint_slot->getPivot();
    btVector3 bt_pivot_in_part = simulator::vec3_eigen_to_bullet(pivot);

    //this->bulletTypedConstraint = new btFixedConstraint(*bt_rigid_body, bt_pivot_in_part);
    btVector3 bt_axis(0, 0, 1);
    btHingeConstraint * p_hinge_constraint = new btHingeConstraint(*bt_rigid_body, bt_pivot_in_part, bt_axis);
    p_hinge_constraint->setLimit(low, high, softness, bias_factor, relaxation_factor);
    this->bulletTypedConstraint = p_hinge_constraint;
}

simulator::Fixed::~Fixed() {
    // TODO
}

std::string simulator::Fixed::getName() const {
    return this->name;
}

