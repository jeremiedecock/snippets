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

botsim::Motor::Motor(botsim::Part * part1,
                        botsim::Part * part2,
                        botsim::HingeSlot * joint_slot_for_part1,
                        botsim::HingeSlot * joint_slot_for_part2,
                        std::string _name) //:
                            // call superclass (hinge) constructor
                            //botsim::Hinge(part1, part2, pivot_in_part1, pivot_in_part2, axis_in_part1, axis_in_part2, _name) {
                        {
    // TODO ?

    this->name = _name;

    btRigidBody * bt_rigid_body1 = part1->getRigidBody();
    btRigidBody * bt_rigid_body2 = part2->getRigidBody();

    Eigen::Vector3d pivot_in_part1 = joint_slot_for_part1->getPivot();
    Eigen::Vector3d pivot_in_part2 = joint_slot_for_part2->getPivot();
    btVector3 bt_pivot_in_part1 = botsim::vec3_eigen_to_bullet(pivot_in_part1);
    btVector3 bt_pivot_in_part2 = botsim::vec3_eigen_to_bullet(pivot_in_part2);

    Eigen::Vector3d axis_in_part1 = joint_slot_for_part1->getAxis();
    Eigen::Vector3d axis_in_part2 = joint_slot_for_part2->getAxis();
    btVector3 bt_axis_in_part1 = botsim::vec3_eigen_to_bullet(axis_in_part1);
    btVector3 bt_axis_in_part2 = botsim::vec3_eigen_to_bullet(axis_in_part2);

    this->bulletTypedConstraint = new btHingeConstraint(*bt_rigid_body1, *bt_rigid_body2, bt_pivot_in_part1, bt_pivot_in_part2, bt_axis_in_part1, bt_axis_in_part2);
}

botsim::Motor::Motor(botsim::Part * part,
                        botsim::HingeSlot * joint_slot,
                        std::string _name) //:
                            // call superclass (hinge) constructor
                            //botsim::Hinge(part, pivot, axis, _name) {
                            {
    // TODO ?

    this->name = _name;

    btRigidBody * bt_rigid_body = part->getRigidBody();

    Eigen::Vector3d pivot = joint_slot->getPivot();
    btVector3 bt_pivot_in_part = botsim::vec3_eigen_to_bullet(pivot);

    Eigen::Vector3d axis = joint_slot->getAxis();
    btVector3 bt_axis_in_part = botsim::vec3_eigen_to_bullet(axis);

    this->bulletTypedConstraint = new btHingeConstraint(*bt_rigid_body, bt_pivot_in_part, bt_axis_in_part);
}

botsim::Motor::~Motor() {
    // TODO
}

void botsim::Motor::setAngularVelocity(double target_velocity) {
    if(btHingeConstraint * hinge_constraint = dynamic_cast<btHingeConstraint *>(this->bulletTypedConstraint)) {
        bool enable_motor = true;        // TODO
        double max_motor_impulse = 5000.;   // TODO
        hinge_constraint->enableAngularMotor(enable_motor, target_velocity, max_motor_impulse);
    } else {
        throw std::invalid_argument("Internal error."); 
    }

}

std::string botsim::Motor::getName() const {
    return this->name;
}
