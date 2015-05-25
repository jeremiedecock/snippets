/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "logger_time_steps_parts_json.h"
#include "tools/tools.h"

#include <iostream>

const std::string DEFAULT_FILE_PATH = "time_steps_parts.json"; // TODO ?

botsim::LoggerTimeStepsPartsJson::LoggerTimeStepsPartsJson(std::set<botsim::Part *> observed_part_set, std::string filepath) {
    // Set the observed parts set
    this->observedPartSet = observed_part_set;

    // TODO: if a part is not in the environment, remove it from the set ?
    //// Set logged parts
    //std::set<Part *>::iterator it;
    //for(it = observed_part_set.begin() ; it != observed_part_set.end() ; it++) {
    //    this->attach(*it);
    //}

    // Set filepath
    if(filepath == "") {
        this->filepath = DEFAULT_FILE_PATH;
    } else {
        this->filepath = filepath;
    }
    
    // Open the log file
    std::cout << "Open " << this->filepath << std::endl;
    this->ofs = new std::ofstream(this->filepath.c_str());

    // Initialize the dataMap
    this->dataMap = std::map<std::string, std::vector<double> >();

    this->dataMap["elapsed_simulation_time_sec"] = std::vector<double>();

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();

        this->dataMap[part_name + "_position_x"] = std::vector<double>();
        this->dataMap[part_name + "_position_y"] = std::vector<double>();
        this->dataMap[part_name + "_position_z"] = std::vector<double>();

        this->dataMap[part_name + "_angle_x"] = std::vector<double>();
        this->dataMap[part_name + "_angle_y"] = std::vector<double>();
        this->dataMap[part_name + "_angle_z"] = std::vector<double>();
        this->dataMap[part_name + "_angle_w"] = std::vector<double>();

        this->dataMap[part_name + "_linear_velocity_x"] = std::vector<double>();
        this->dataMap[part_name + "_linear_velocity_y"] = std::vector<double>();
        this->dataMap[part_name + "_linear_velocity_z"] = std::vector<double>();

        this->dataMap[part_name + "_angular_velocity_x"] = std::vector<double>();
        this->dataMap[part_name + "_angular_velocity_y"] = std::vector<double>();
        this->dataMap[part_name + "_angular_velocity_z"] = std::vector<double>();

        this->dataMap[part_name + "_total_force_x"] = std::vector<double>();
        this->dataMap[part_name + "_total_force_y"] = std::vector<double>();
        this->dataMap[part_name + "_total_force_z"] = std::vector<double>();

        this->dataMap[part_name + "_total_troque_x"] = std::vector<double>();
        this->dataMap[part_name + "_total_troque_y"] = std::vector<double>();
        this->dataMap[part_name + "_total_troque_z"] = std::vector<double>();
    }
}

botsim::LoggerTimeStepsPartsJson::~LoggerTimeStepsPartsJson() {
    // Write the json file
    (* this->ofs) << "{" << std::endl;
    std::map<std::string, std::vector<double> >::iterator it;
    for(it = this->dataMap.begin() ; it != this->dataMap.end() ; it++) {
        if(it != this->dataMap.begin()) {
            // Finish the previous line
            // (because the last item of the Json map should not be ended with a comma).
            (* this->ofs) << "," << std::endl;
        }

        (* this->ofs) << "    \"" << it->first << "\": [" << botsim::vector_to_string(it->second, ", ") << "]";
    }
    (* this->ofs) << std::endl << "}" << std::endl;

    // Close the log file
    std::cout << "Close " << this->filepath << std::endl;
    this->ofs->flush();
    this->ofs->close();

    // Destroy dynamic objects
    delete this->ofs;
}

void botsim::LoggerTimeStepsPartsJson::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();
    this->dataMap["elapsed_simulation_time_sec"].push_back(elapsed_simulation_time_sec);

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();

        const Eigen::Vector3d part_position         = (*it)->getPosition();
        const Eigen::Vector4d part_angle            = (*it)->getAngle();
        const Eigen::Vector3d part_linear_velocity  = (*it)->getLinearVelocity();
        const Eigen::Vector3d part_angular_velicity = (*it)->getAngularVelocity();
        const Eigen::Vector3d part_total_force      = (*it)->getTotalForce();
        const Eigen::Vector3d part_total_torque     = (*it)->getTotalTorque();

        this->dataMap[part_name + "_position_x"].push_back(part_position[0]);
        this->dataMap[part_name + "_position_y"].push_back(part_position[1]);
        this->dataMap[part_name + "_position_z"].push_back(part_position[2]);

        this->dataMap[part_name + "_angle_x"].push_back(part_angle[0]);
        this->dataMap[part_name + "_angle_y"].push_back(part_angle[1]);
        this->dataMap[part_name + "_angle_z"].push_back(part_angle[2]);
        this->dataMap[part_name + "_angle_w"].push_back(part_angle[3]);

        this->dataMap[part_name + "_linear_velocity_x"].push_back(part_linear_velocity[0]);
        this->dataMap[part_name + "_linear_velocity_y"].push_back(part_linear_velocity[1]);
        this->dataMap[part_name + "_linear_velocity_z"].push_back(part_linear_velocity[2]);

        this->dataMap[part_name + "_angular_velocity_x"].push_back(part_angular_velicity[0]);
        this->dataMap[part_name + "_angular_velocity_y"].push_back(part_angular_velicity[1]);
        this->dataMap[part_name + "_angular_velocity_z"].push_back(part_angular_velicity[2]);

        this->dataMap[part_name + "_total_force_x"].push_back(part_total_force[0]);
        this->dataMap[part_name + "_total_force_y"].push_back(part_total_force[1]);
        this->dataMap[part_name + "_total_force_z"].push_back(part_total_force[2]);

        this->dataMap[part_name + "_total_troque_x"].push_back(part_total_torque[0]);
        this->dataMap[part_name + "_total_troque_y"].push_back(part_total_torque[1]);
        this->dataMap[part_name + "_total_troque_z"].push_back(part_total_torque[2]);
    }
}

std::string botsim::LoggerTimeStepsPartsJson::getFilepath() const {
    return this->filepath;
}
