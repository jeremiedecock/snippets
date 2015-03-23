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

simulator::LoggerTimeStepsPartsJson::LoggerTimeStepsPartsJson(std::set<simulator::Part *> observed_parts_set, std::string filepath) {
    // Set the observed parts set
    this->observedPartSet = observed_parts_set;

    // TODO: if a part is not in the environment, remove it from the set ?
    //// Set logged parts
    //std::set<Part *>::iterator it;
    //for(it = observed_parts_set.begin() ; it != observed_parts_set.end() ; it++) {
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
    }
}

simulator::LoggerTimeStepsPartsJson::~LoggerTimeStepsPartsJson() {
    // Write the json file
    (* this->ofs) << "{" << std::endl;
    std::map<std::string, std::vector<double> >::iterator it;
    for(it = this->dataMap.begin() ; it != this->dataMap.end() ; it++) {
        if(it != this->dataMap.begin()) {
            // Finish the previous line
            // (because the last item of the Json map should not be ended with a comma).
            (* this->ofs) << "," << std::endl;
        }

        (* this->ofs) << "    \"" << it->first << "\": [" << simulator::vector_to_string(it->second, ", ") << "]";
    }
    (* this->ofs) << std::endl << "}" << std::endl;

    // Close the log file
    std::cout << "Close " << this->filepath << std::endl;
    this->ofs->flush();
    this->ofs->close();

    // Destroy dynamic objects
    delete this->ofs;
}

void simulator::LoggerTimeStepsPartsJson::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();
    this->dataMap["elapsed_simulation_time_sec"].push_back(elapsed_simulation_time_sec);

    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        std::string part_name = (*it)->getName();
        const Eigen::Vector3d part_position = (*it)->getPosition();

        this->dataMap[part_name + "_position_x"].push_back(part_position[0]);
        this->dataMap[part_name + "_position_y"].push_back(part_position[1]);
        this->dataMap[part_name + "_position_z"].push_back(part_position[2]);
    }
}

std::string simulator::LoggerTimeStepsPartsJson::getFilepath() const {
    return this->filepath;
}
