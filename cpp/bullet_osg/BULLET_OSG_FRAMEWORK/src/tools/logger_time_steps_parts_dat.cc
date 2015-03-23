/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "logger_time_steps_parts_dat.h"
#include "tools/tools.h"

#include <iostream>

simulator::LoggerTimeStepsPartsDat::LoggerTimeStepsPartsDat(std::set<simulator::Part *> observed_parts_set) {
    // Set the observed parts set
    this->observedPartSet = observed_parts_set;
    
    // Initialize the fileMap
    this->fileMap = std::map<std::string, std::ofstream *>();

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + ".dat";

        // Open the log file
        std::cout << "Open " << file_path << std::endl;
        this->fileMap[file_path] = new std::ofstream(file_path.c_str());

        // Write the header
        (* this->fileMap[file_path]) << "#time(sec) position_x position_y position_z" << std::endl; // TODO
    }
}

simulator::LoggerTimeStepsPartsDat::~LoggerTimeStepsPartsDat() {
    // Close the log file
    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + ".dat";

        // Open the log file
        std::cout << "Close " << file_path << std::endl;
        this->fileMap[file_path]->flush();
        this->fileMap[file_path]->close();

        delete this->fileMap[file_path];
    }
}

void simulator::LoggerTimeStepsPartsDat::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        std::string file_path = part_name + ".dat";

        Eigen::Vector3d position_vector = (*it)->getPosition();

        (* this->fileMap[file_path]) << elapsed_simulation_time_sec  << " " << simulator::eigen_vector_to_string(position_vector, " ") << std::endl;
    }
}
