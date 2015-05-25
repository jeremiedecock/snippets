/* 
 * Bullet OSG Framework.
 * Robudog JD module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "actuator.h"
#include "actuators/motor.h"

#include "builtin_parts/dynamixel_ax12.h"
#include "builtin_parts/robudog_trunk.h"

#include "joint.h"
#include "joints/point_to_point.h"
#include "joints/fixed.h"
#include "joint_slots/hinge_slot.h"
#include "joint_slots/point_to_point_slot.h"
#include "joint_slots/fixed_slot.h"

#include "parts/box.h"

#include "robudog_jd.h"

#include <iostream>
#include <set>

#include <Eigen/Dense>

static const double ax12_size_x = 2.5;  // TODO !!!
static const double ax12_size_y = 3.5 + 0.5;  // TODO !!!
static const double ax12_size_z = 5. + 2.5;  // TODO !!!

static const double trunk_size_x = 20.;  // TODO !!!
static const double trunk_size_y = 7.5;  // TODO !!!
static const double trunk_size_z = 5.;   // TODO !!!

static const double foot_radius = 1.25;  // TODO !!!

/*
 *
 */

// TODO: put this as a static method in the "Fixed" class.
void addFixedJoint(std::set<botsim::Joint *> & joint_set,
                   botsim::Part * p_part,
                   std::string slot_key,
                   std::string joint_name) {

        botsim::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        if(botsim::FixedSlot * p_fixed_slot = dynamic_cast<botsim::FixedSlot *>(p_joint_slot)) {
            botsim::Fixed * p_joint = new botsim::Fixed(p_part, p_fixed_slot, joint_name);
            joint_set.insert(p_joint);
        } else {
            throw std::invalid_argument(slot_key + " is not a \"Fixed Slot\".");
        }

}

// TODO: put this as a static method in the "PointToPoint" class.
void addP2PJoint(std::set<botsim::Joint *> & joint_set,
                 botsim::Part * p_part,
                 std::string slot_key,
                 std::string joint_name) {

        botsim::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        if(botsim::PointToPointSlot * p_p2p_slot = dynamic_cast<botsim::PointToPointSlot *>(p_joint_slot)) {
            botsim::PointToPoint * p_joint = new botsim::PointToPoint(p_part, p_p2p_slot, joint_name);
            joint_set.insert(p_joint);
        } else {
            throw std::invalid_argument(slot_key + " is not a \"Point To Point Slot\".");
        }

}

// TODO: put this as a static method in the "Hinge" class (pb: actuator_set vs joint_set -> template ? ou mettre la version actuator dans Motor ?).
void addMotor(std::set<botsim::Actuator *> & actuator_set,
              botsim::Part * p_part1,
              botsim::Part * p_part2,
              std::string slot_key1,
              std::string slot_key2,
              std::string actuator_name) {

        botsim::JointSlot * p_joint_slot1 = p_part1->getJointSlot(slot_key1);
        botsim::HingeSlot * p_hinge_slot1 = dynamic_cast<botsim::HingeSlot *>(p_joint_slot1);

        botsim::JointSlot * p_joint_slot2 = p_part2->getJointSlot(slot_key2);
        botsim::HingeSlot * p_hinge_slot2 = dynamic_cast<botsim::HingeSlot *>(p_joint_slot2);

        if(p_hinge_slot1 == NULL) {
            throw std::invalid_argument(slot_key1 + " is not a \"Hinge Slot\".");
        } else if(p_hinge_slot2 == NULL) {
            throw std::invalid_argument(slot_key2 + " is not a \"Hinge Slot\".");
        } else {
            botsim::Motor * p_motor = new botsim::Motor(p_part1, p_part2, p_hinge_slot1, p_hinge_slot2, actuator_name);
            actuator_set.insert(p_motor);
        }
}

// TODO: put this as a static method in the "Hinge" class (pb: actuator_set vs joint_set -> template ? ou mettre la version actuator dans Motor ?).
void addMotor(std::set<botsim::Actuator *> & actuator_set,
              botsim::Part * p_part,
              std::string slot_key,
              std::string actuator_name) {

        botsim::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        botsim::HingeSlot * p_hinge_slot = dynamic_cast<botsim::HingeSlot *>(p_joint_slot);

        if(p_hinge_slot == NULL) {
            throw std::invalid_argument(slot_key + " is not a \"Hinge Slot\".");
        } else {
            botsim::Motor * p_motor = new botsim::Motor(p_part, p_hinge_slot, actuator_name);
            actuator_set.insert(p_motor);
        }
}


botsim::Object * botsim::make_robudog_jd(const Eigen::Vector3d object_initial_position, std::string object_name) {

    /*
     * ROBUDOG PARTS
     */
    
    std::set<botsim::Part *> robudog_part_set;

    // Trunk ////////////////////
    botsim::Part * p_robudog_trunk_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(0. + object_initial_position[0],
                                                                 0. + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z * 2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("trunk");

        p_robudog_trunk_part = botsim::make_robudog_trunk(initial_position, initial_angle, name);
        robudog_part_set.insert(p_robudog_trunk_part);
    }

    // UPPER PARTS //////////////////////////////

    // Head /////////////////////
    
    // Left clavicle ////////////
    
    // Right clavicle ///////////
    
    // Left shoulder ////////////
    
    // Right shoulder ///////////
    
    // Left upper arm ///////////
    botsim::Part * p_ax12_left_upper_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.) + object_initial_position[0],
                                                                 trunk_size_y/2. + ax12_size_y/2. + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_upper_arm");

        p_ax12_left_upper_arm_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_upper_arm_part);
    }
    
    // Right upper arm //////////
    botsim::Part * p_ax12_right_upper_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.) + object_initial_position[0],
                                                                 -(trunk_size_y/2. + ax12_size_y/2.) + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_upper_arm");

        p_ax12_right_upper_arm_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_upper_arm_part);
    }
    
    // Left fore arm ////////////
    botsim::Part * p_ax12_left_fore_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.) + object_initial_position[0],
                                                                 trunk_size_y/2. + ax12_size_y/2. + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_fore_arm");

        p_ax12_left_fore_arm_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_fore_arm_part);
    }
    
    // Right fore arm ///////////
    botsim::Part * p_ax12_right_fore_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.) + object_initial_position[0],
                                                                 -(trunk_size_y/2. + ax12_size_y/2.) + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_fore_arm");

        p_ax12_right_fore_arm_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_fore_arm_part);
    }
    
    // Left fore foot ///////////
    
    // Right fore foot //////////

    // LOWER PARTS //////////////////////////////
    
    // Left hip /////////////////
    
    // Right hip ////////////////
    
    // Left thigh ///////////////
    botsim::Part * p_ax12_left_thigh_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.) + object_initial_position[0],
                                                                 trunk_size_y/2. + ax12_size_y/2. + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_thigh");

        p_ax12_left_thigh_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_thigh_part);
    }
    
    // Right thigh //////////////
    botsim::Part * p_ax12_right_thigh_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.) + object_initial_position[0],
                                                                 -(trunk_size_y/2. + ax12_size_y/2.) + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_thigh");

        p_ax12_right_thigh_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_thigh_part);
    }
    
    // Left shin ////////////////
    botsim::Part * p_ax12_left_shin_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.) + object_initial_position[0],
                                                                 trunk_size_y/2. + ax12_size_y/2. + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_shin");

        p_ax12_left_shin_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_shin_part);
    }
    
    // Right shin ///////////////
    botsim::Part * p_ax12_right_shin_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.) + object_initial_position[0],
                                                                 -(trunk_size_y/2. + ax12_size_y/2.) + object_initial_position[1],
                                                                 foot_radius * 2. + ax12_size_z/2. + object_initial_position[2]);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_shin");

        p_ax12_right_shin_part = botsim::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_shin_part);
    }
    
    // Left hind foot ///////////
    
    // Right hind foot //////////

    /*
     * ROBUDOG JOINTS
     */

    std::set<botsim::Joint *> robudog_joint_set;

    // Trunk - crane //////////////////
    //addFixedJoint(robudog_joint_set, p_robudog_trunk_part, "crane", "crane_joint");

    /*
     * ROBUDOG ACTUATORS
     */
    
    std::set<botsim::Actuator *> robudog_actuator_set;
    
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_right_upper_arm_part, "right_shoulder", "slot1", "right_shoulder_motor");
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_left_upper_arm_part, "left_shoulder", "slot1", "left_shoulder_motor");
    //addMotor(robudog_actuator_set, p_ax12_right_upper_arm_part, "slot1", "right_shoulder_motor");
    //addMotor(robudog_actuator_set, p_ax12_left_upper_arm_part,  "slot1", "left_shoulder_motor");
    addMotor(robudog_actuator_set, p_ax12_right_upper_arm_part, p_ax12_right_fore_arm_part, "slot2", "slot1", "right_elbow_motor");
    addMotor(robudog_actuator_set, p_ax12_left_upper_arm_part,  p_ax12_left_fore_arm_part,  "slot2", "slot1", "left_elbow_motor");

    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_right_thigh_part, "right_hip", "slot1", "right_hip_motor");
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_left_thigh_part, "left_hip", "slot1", "left_hip_motor");
    //addMotor(robudog_actuator_set, p_ax12_right_thigh_part, "slot1", "right_hip_motor");
    //addMotor(robudog_actuator_set, p_ax12_left_thigh_part,  "slot1", "left_hip_motor");
    addMotor(robudog_actuator_set, p_ax12_right_thigh_part, p_ax12_right_shin_part, "slot2", "slot1", "right_knee_motor");
    addMotor(robudog_actuator_set, p_ax12_left_thigh_part,  p_ax12_left_shin_part,  "slot2", "slot1", "left_knee_motor");

    /*
     * ROBUDOG OBJECT
     */

    botsim::Object * p_robudog = new botsim::Object(robudog_part_set, robudog_joint_set, robudog_actuator_set, object_name);

    return p_robudog;
}

