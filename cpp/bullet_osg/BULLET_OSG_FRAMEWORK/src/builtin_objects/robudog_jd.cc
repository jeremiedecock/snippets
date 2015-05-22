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

#include "joint.h"
#include "joint_slots/hinge_slot.h"

#include "parts/box.h"

#include "robudog_jd.h"

#include <iostream>
#include <set>

#include <Eigen/Dense>

simulator::Object * simulator::make_robudog_jd() {

    // Robudog parts
    simulator::Part * p_ax12_part = simulator::make_dynamixel_ax12();

    std::set<simulator::Part *> robudog_part_set;
    robudog_part_set.insert(p_ax12_part);

    // Robudog joints
    std::set<simulator::Joint *> robudog_joint_set;

    // Robudog actuators
    std::set<simulator::Actuator *> robudog_actuator_set;
    
    std::map<std::string, simulator::JointSlot *>::iterator it;
    simulator::JointSlot * p_joint_slot;
    simulator::HingeSlot * p_hinge_slot;

    for(it = p_ax12_part->jointSlotMap.begin() ; it != p_ax12_part->jointSlotMap.end() ; it++) {
        std::cout << "name : " << it->first << std::endl;
        std::cout << "address : " << it->second << std::endl;
    }

    it = p_ax12_part->jointSlotMap.find(std::string("slot1")); 
    if(it != p_ax12_part->jointSlotMap.end()) {
        p_joint_slot = it->second;
        if(p_joint_slot != NULL) {
            p_hinge_slot = dynamic_cast<simulator::HingeSlot *>(p_joint_slot); // TODO: HUGLY WORKAROUND !
            simulator::Motor * p_robudog_motor = new simulator::Motor(p_ax12_part, p_hinge_slot, "robudog_motor");
            robudog_actuator_set.insert(p_robudog_motor);
        } else {
            std::cout << "ERROR" << std::endl;
        }
    }

    // Robudog object
    simulator::Object * p_robudog = new simulator::Object(robudog_part_set, robudog_joint_set, robudog_actuator_set, "robudog");

    return p_robudog;
}

