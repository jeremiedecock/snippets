/* 
 * Bullet OSG Framework.
 * Dynamixel AX-12 module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "dynamixel_ax12.h"

#include "joint_slots/hinge_slot.h"

#include "parts/box.h"

#include <Eigen/Dense>

#include <iostream>
#include <string>

/*
 * PART'S PROPERTIES
 */

static const Eigen::Vector3d initial_dimension = Eigen::Vector3d(2.5, 3.5, 5.);
//static const Eigen::Vector3d initial_position = Eigen::Vector3d(0., 0., 5.);
//static const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
static const Eigen::Vector3d initial_velocity = Eigen::Vector3d(0., 0., 0.);
static const Eigen::Vector3d initial_angular_velocity = Eigen::Vector3d(0., 0., 0.);
static const Eigen::Vector3d initial_inertia = Eigen::Vector3d(0., 0., 0.);
static const double mass = 5.;
static double friction = 0.5;
static double rolling_friction = 0.;
static double restitution = 0.;

simulator::Part * simulator::make_dynamixel_ax12(const Eigen::Vector3d initial_position, const Eigen::Vector4d initial_angle, std::string name) {

    // Make the part
    simulator::Part * p_part = new simulator::Box(initial_dimension,
                                                  initial_position,
                                                  initial_angle,
                                                  initial_velocity,
                                                  initial_angular_velocity,
                                                  initial_inertia,
                                                  mass,
                                                  friction,
                                                  rolling_friction,
                                                  restitution,
                                                  name);
    

    // Add joint slot 1
    Eigen::Vector3d robudog_hinge_pivot_1(0., 0., 1.5);
    Eigen::Vector3d robudog_hinge_axis_1(0., 1., 0.);
    simulator::HingeSlot * p_robudog_joint_slot_1 = new simulator::HingeSlot(robudog_hinge_pivot_1, robudog_hinge_axis_1);

    // Add joint slot 2
    Eigen::Vector3d robudog_hinge_pivot_2(0., 0., -5.);  // -2.5 - 2.5
    Eigen::Vector3d robudog_hinge_axis_2(0., 1., 0.);
    simulator::HingeSlot * p_robudog_joint_slot_2 = new simulator::HingeSlot(robudog_hinge_pivot_2, robudog_hinge_axis_2);

    p_part->addJointSlot(std::string("slot1"), p_robudog_joint_slot_1);
    p_part->addJointSlot(std::string("slot2"), p_robudog_joint_slot_2);

    return p_part;
}

