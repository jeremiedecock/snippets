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

static const double height = 0.5;        // TODO !!!

/*
 *
 */

// TODO: put this as a static method in the "Fixed" class.
void addFixedJoint(std::set<simulator::Joint *> & joint_set,
                   simulator::Part * p_part,
                   std::string slot_key,
                   std::string joint_name) {

        simulator::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        if(simulator::FixedSlot * p_fixed_slot = dynamic_cast<simulator::FixedSlot *>(p_joint_slot)) {
            simulator::Fixed * p_joint = new simulator::Fixed(p_part, p_fixed_slot, joint_name);
            joint_set.insert(p_joint);
        } else {
            throw std::invalid_argument(slot_key + " is not a \"Fixed Slot\".");
        }

}

// TODO: put this as a static method in the "PointToPoint" class.
void addP2PJoint(std::set<simulator::Joint *> & joint_set,
                 simulator::Part * p_part,
                 std::string slot_key,
                 std::string joint_name) {

        simulator::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        if(simulator::PointToPointSlot * p_p2p_slot = dynamic_cast<simulator::PointToPointSlot *>(p_joint_slot)) {
            simulator::PointToPoint * p_joint = new simulator::PointToPoint(p_part, p_p2p_slot, joint_name);
            joint_set.insert(p_joint);
        } else {
            throw std::invalid_argument(slot_key + " is not a \"Point To Point Slot\".");
        }

}

// TODO: put this as a static method in the "Hinge" class (pb: actuator_set vs joint_set -> template ? ou mettre la version actuator dans Motor ?).
void addMotor(std::set<simulator::Actuator *> & actuator_set,
              simulator::Part * p_part1,
              simulator::Part * p_part2,
              std::string slot_key1,
              std::string slot_key2,
              std::string actuator_name) {

        simulator::JointSlot * p_joint_slot1 = p_part1->getJointSlot(slot_key1);
        simulator::HingeSlot * p_hinge_slot1 = dynamic_cast<simulator::HingeSlot *>(p_joint_slot1);

        simulator::JointSlot * p_joint_slot2 = p_part2->getJointSlot(slot_key2);
        simulator::HingeSlot * p_hinge_slot2 = dynamic_cast<simulator::HingeSlot *>(p_joint_slot2);

        if(p_hinge_slot1 == NULL) {
            throw std::invalid_argument(slot_key1 + " is not a \"Hinge Slot\".");
        } else if(p_hinge_slot2 == NULL) {
            throw std::invalid_argument(slot_key2 + " is not a \"Hinge Slot\".");
        } else {
            simulator::Motor * p_motor = new simulator::Motor(p_part1, p_part2, p_hinge_slot1, p_hinge_slot2, actuator_name);
            actuator_set.insert(p_motor);
        }
}

// TODO: put this as a static method in the "Hinge" class (pb: actuator_set vs joint_set -> template ? ou mettre la version actuator dans Motor ?).
void addMotor(std::set<simulator::Actuator *> & actuator_set,
              simulator::Part * p_part,
              std::string slot_key,
              std::string actuator_name) {

        simulator::JointSlot * p_joint_slot = p_part->getJointSlot(slot_key);
        simulator::HingeSlot * p_hinge_slot = dynamic_cast<simulator::HingeSlot *>(p_joint_slot);

        if(p_hinge_slot == NULL) {
            throw std::invalid_argument(slot_key + " is not a \"Hinge Slot\".");
        } else {
            simulator::Motor * p_motor = new simulator::Motor(p_part, p_hinge_slot, actuator_name);
            actuator_set.insert(p_motor);
        }
}


simulator::Object * simulator::make_robudog_jd() {

    /*
     * ROBUDOG PARTS
     */
    
    std::set<simulator::Part *> robudog_part_set;

    // Trunk ////////////////////
    simulator::Part * p_robudog_trunk_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(0.,
                                                                 0.,
                                                                 foot_radius * 2. + ax12_size_z * 2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("trunk");

        p_robudog_trunk_part = simulator::make_robudog_trunk(initial_position, initial_angle, name);
        robudog_part_set.insert(p_robudog_trunk_part);
    }

    // UPPER PARTS //////////////////////////////

    // Head /////////////////////
    
    // Left clavicle ////////////
    
    // Right clavicle ///////////
    
    // Left shoulder ////////////
    
    // Right shoulder ///////////
    
    // Left upper arm ///////////
    simulator::Part * p_ax12_left_upper_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.),
                                                                 trunk_size_y/2. + ax12_size_y/2.,
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_upper_arm");

        p_ax12_left_upper_arm_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_upper_arm_part);
    }
    
    // Right upper arm //////////
    simulator::Part * p_ax12_right_upper_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.),
                                                                 -(trunk_size_y/2. + ax12_size_y/2.),
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_upper_arm");

        p_ax12_right_upper_arm_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_upper_arm_part);
    }
    
    // Left fore arm ////////////
    simulator::Part * p_ax12_left_fore_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.),
                                                                 trunk_size_y/2. + ax12_size_y/2.,
                                                                 foot_radius * 2. + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_fore_arm");

        p_ax12_left_fore_arm_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_fore_arm_part);
    }
    
    // Right fore arm ///////////
    simulator::Part * p_ax12_right_fore_arm_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(trunk_size_x/2. - (ax12_size_x/2.),
                                                                 -(trunk_size_y/2. + ax12_size_y/2.),
                                                                 foot_radius * 2. + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_fore_arm");

        p_ax12_right_fore_arm_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_fore_arm_part);
    }
    
    // Left fore foot ///////////
    
    // Right fore foot //////////

    // LOWER PARTS //////////////////////////////
    
    // Left hip /////////////////
    
    // Right hip ////////////////
    
    // Left thigh ///////////////
    simulator::Part * p_ax12_left_thigh_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.),
                                                                 trunk_size_y/2. + ax12_size_y/2.,
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_thigh");

        p_ax12_left_thigh_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_thigh_part);
    }
    
    // Right thigh //////////////
    simulator::Part * p_ax12_right_thigh_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.),
                                                                 -(trunk_size_y/2. + ax12_size_y/2.),
                                                                 foot_radius * 2. + ax12_size_z + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_thigh");

        p_ax12_right_thigh_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_thigh_part);
    }
    
    // Left shin ////////////////
    simulator::Part * p_ax12_left_shin_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.),
                                                                 trunk_size_y/2. + ax12_size_y/2.,
                                                                 foot_radius * 2. + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("left_shin");

        p_ax12_left_shin_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_left_shin_part);
    }
    
    // Right shin ///////////////
    simulator::Part * p_ax12_right_shin_part;
    {
        const Eigen::Vector3d initial_position = Eigen::Vector3d(-trunk_size_x/2. + (ax12_size_x/2.),
                                                                 -(trunk_size_y/2. + ax12_size_y/2.),
                                                                 foot_radius * 2. + ax12_size_z/2. + height);
        const Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
        const std::string name("right_shin");

        p_ax12_right_shin_part = simulator::make_dynamixel_ax12(initial_position, initial_angle, name);
        robudog_part_set.insert(p_ax12_right_shin_part);
    }
    
    // Left hind foot ///////////
    
    // Right hind foot //////////

    /*
     * ROBUDOG JOINTS
     */

    std::set<simulator::Joint *> robudog_joint_set;

    // Trunk - crane //////////////////
    addFixedJoint(robudog_joint_set, p_robudog_trunk_part, "crane", "crane_joint");

    /*
     * ROBUDOG ACTUATORS
     */
    
    std::set<simulator::Actuator *> robudog_actuator_set;
    
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_right_upper_arm_part, "right_shoulder", "slot1", "right_shoulder_motor");
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_left_upper_arm_part, "left_shoulder", "slot1", "left_shoulder_motor");
    //addMotor(robudog_actuator_set, p_ax12_right_upper_arm_part, "slot1", "right_shoulder_motor");
    //addMotor(robudog_actuator_set, p_ax12_left_upper_arm_part,  "slot1", "left_shoulder_motor");
    addMotor(robudog_actuator_set, p_ax12_right_upper_arm_part, p_ax12_right_fore_arm_part, "slot2", "slot1", "right_elbow_motor");
    addMotor(robudog_actuator_set, p_ax12_left_upper_arm_part,  p_ax12_left_fore_arm_part,  "slot2", "slot1", "left_elbow_motor");

    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_right_thigh_part, "right_hip", "slot1", "right_shoulder_motor");
    addMotor(robudog_actuator_set, p_robudog_trunk_part, p_ax12_left_thigh_part, "left_hip", "slot1", "left_shoulder_motor");
    //addMotor(robudog_actuator_set, p_ax12_right_thigh_part, "slot1", "right_hip_motor");
    //addMotor(robudog_actuator_set, p_ax12_left_thigh_part,  "slot1", "left_hip_motor");
    addMotor(robudog_actuator_set, p_ax12_right_thigh_part, p_ax12_right_shin_part, "slot2", "slot1", "right_knee_motor");
    addMotor(robudog_actuator_set, p_ax12_left_thigh_part,  p_ax12_left_shin_part,  "slot2", "slot1", "left_knee_motor");

    /*
     * ROBUDOG OBJECT
     */

    simulator::Object * p_robudog = new simulator::Object(robudog_part_set, robudog_joint_set, robudog_actuator_set, "robudog");

    return p_robudog;
}

