/* 
 * Bullet OSG Framework.
 * Robudog trunk module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "robudog_trunk.h"

#include "joint_slots/fixed_slot.h"
#include "joint_slots/hinge_slot.h"
#include "joint_slots/point_to_point_slot.h"

#include "parts/box.h"

#include <Eigen/Dense>

#include <iostream>
#include <string>

/*
 * PART'S PROPERTIES
 */

static const Eigen::Vector3d initial_dimension = Eigen::Vector3d(20., 7.5, 5.);
//static const Eigen::Vector3d initial_position = Eigen::Vector3d(0., 0., 5.);
//static const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
static const Eigen::Vector3d initial_velocity = Eigen::Vector3d(0., 0., 0.);
static const Eigen::Vector3d initial_angular_velocity = Eigen::Vector3d(0., 0., 0.);
static const Eigen::Vector3d initial_inertia = Eigen::Vector3d(0., 0., 0.);
static const double mass = 5.;
static double friction = 0.5;
static double rolling_friction = 0.;
static double restitution = 0.;

botsim::Part * botsim::make_robudog_trunk(const Eigen::Vector3d initial_position, const Eigen::Vector4d initial_angle, std::string name) {

    // Make the part
    botsim::Part * p_part = new botsim::Box(initial_dimension,
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
    

    const double dim_x = initial_dimension[0];
    const double dim_y = initial_dimension[1];
    const double dim_z = initial_dimension[2];
    
    const double dim_ax12_x = 2.5; // TODO !!!
    const double dim_ax12_y = 3.5 + 0.5; // TODO !!!
    const double dim_ax12_z = 5.;  // TODO !!!

    // Add left shoulder joint slot
    Eigen::Vector3d left_shoulder_pivot(dim_x/2. - dim_ax12_x/2., dim_y/2. + dim_ax12_y/2., 0.);
    Eigen::Vector3d left_shoulder_axis(0., 1., 0.);
    botsim::HingeSlot * p_left_shoulder_joint_slot = new botsim::HingeSlot(left_shoulder_pivot, left_shoulder_axis);

    // Add right shoulder joint slot
    Eigen::Vector3d right_shoulder_pivot(dim_x/2. - dim_ax12_x/2., -dim_y/2. - dim_ax12_y/2., 0.);
    Eigen::Vector3d right_shoulder_axis(0., 1., 0.);
    botsim::HingeSlot * p_right_shoulder_joint_slot = new botsim::HingeSlot(right_shoulder_pivot, right_shoulder_axis);

    // Add left hip joint slot
    Eigen::Vector3d left_hip_pivot(-dim_x/2. + dim_ax12_x/2., dim_y/2. + dim_ax12_y/2., 0.);
    Eigen::Vector3d left_hip_axis(0., 1., 0.);
    botsim::HingeSlot * p_left_hip_joint_slot = new botsim::HingeSlot(left_hip_pivot, left_hip_axis);

    // Add right hip joint slot
    Eigen::Vector3d right_hip_pivot(-dim_x/2. + dim_ax12_x/2., -dim_y/2. - dim_ax12_y/2., 0.);
    Eigen::Vector3d right_hip_axis(0., 1., 0.);
    botsim::HingeSlot * p_right_hip_joint_slot = new botsim::HingeSlot(right_hip_pivot, right_hip_axis);

    // Add crane (machine) joint slot
    Eigen::Vector3d crane_pivot(0., 0., dim_z/2.);
    //botsim::PointToPointSlot * p_crane_joint_slot = new botsim::PointToPointSlot(crane_pivot);
    botsim::FixedSlot * p_crane_joint_slot = new botsim::FixedSlot(crane_pivot);

    p_part->addJointSlot(std::string("left_shoulder"), p_left_shoulder_joint_slot);
    p_part->addJointSlot(std::string("right_shoulder"), p_right_shoulder_joint_slot);
    p_part->addJointSlot(std::string("left_hip"), p_left_hip_joint_slot);
    p_part->addJointSlot(std::string("right_hip"), p_right_hip_joint_slot);
    p_part->addJointSlot(std::string("crane"), p_crane_joint_slot);

    return p_part;
}

