/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "logger_ticks_parts_dat.h"
#include "tools/tools.h"

#include <iostream>

botsim::LoggerTicksPartsDat::LoggerTicksPartsDat(std::set<botsim::Part *> observed_part_set) {
    // Set the observed parts set
    this->observedPartSet = observed_part_set;
    
    // Initialize the fileMap
    this->fileMap = std::map<std::string, std::ofstream *>();

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + "_ticks.dat";

        // Open the log file
        std::cout << "Open " << file_path << std::endl;
        this->fileMap[file_path] = new std::ofstream(file_path.c_str());

        // Write the header
        (* this->fileMap[file_path]) << "#time(sec)  ";
        (* this->fileMap[file_path]) << "position_x position_y position_z  ";
        (* this->fileMap[file_path]) << "angle_x angle_y angle_z angle_w  ";
        (* this->fileMap[file_path]) << "linear_velocity_x linear_velocity_y linear_velocity_z  ";
        (* this->fileMap[file_path]) << "angular_velocity_x angular_velocity_y angular_velocity_z  ";
        (* this->fileMap[file_path]) << "total_force_x total_force_y total_force_z  ";
        (* this->fileMap[file_path]) << "total_troque_x total_torque_y total_torque_z  ";
        (* this->fileMap[file_path]) << std::endl;
    }
}

botsim::LoggerTicksPartsDat::~LoggerTicksPartsDat() {
    // Close the log file
    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + "_ticks.dat";

        // Open the log file
        std::cout << "Close " << file_path << std::endl;
        this->fileMap[file_path]->flush();
        this->fileMap[file_path]->close();

        delete this->fileMap[file_path];
    }
}

void botsim::LoggerTicksPartsDat::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSecTickRes();

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + "_ticks.dat";

        const Eigen::Vector3d position_vector         = (*it)->getPosition();
        const Eigen::Vector4d angle_vector            = (*it)->getAngle();
        const Eigen::Vector3d linear_velocity_vector  = (*it)->getLinearVelocity();
        const Eigen::Vector3d angular_velicity_vector = (*it)->getAngularVelocity();
        const Eigen::Vector3d total_force_vector      = (*it)->getTotalForce();
        const Eigen::Vector3d total_torque_vector     = (*it)->getTotalTorque();

        (* this->fileMap[file_path]) << elapsed_simulation_time_sec << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(position_vector, " ") << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(angle_vector, " ") << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(linear_velocity_vector, " ") << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(angular_velicity_vector, " ") << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(total_force_vector, " ") << " ";
        (* this->fileMap[file_path]) << botsim::eigen_vector_to_string(total_torque_vector, " ") << " ";
        (* this->fileMap[file_path]) << std::endl;
    }
}
