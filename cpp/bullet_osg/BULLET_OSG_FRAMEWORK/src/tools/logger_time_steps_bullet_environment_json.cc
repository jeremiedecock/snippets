/* 
 * Bullet OSG Framework.
 * Bullet environment logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "logger_time_steps_bullet_environment_json.h"
#include "tools/tools.h"

#include <iostream>

const std::string DEFAULT_FILE_PATH = "time_steps_bullet_environment.json"; // TODO ?

simulator::LoggerTimeStepsBulletEnvironmentJson::LoggerTimeStepsBulletEnvironmentJson(std::string filepath) {
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
    this->dataMap["elapsed_user_time_sec"] = std::vector<double>();
    //this->dataMap["time_step_sec"] = std::vector<double>();
    //this->dataMap["fixed_sub_time_step_sec"] = std::vector<double>();
    //this->dataMap["num_sub_steps"] = std::vector<double>();
    //this->dataMap["max_sub_steps"] = std::vector<double>();
}

simulator::LoggerTimeStepsBulletEnvironmentJson::~LoggerTimeStepsBulletEnvironmentJson() {
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

void simulator::LoggerTimeStepsBulletEnvironmentJson::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();
    double elapsed_user_time_sec = bullet_environment->getElapsedUserTimeSec();
    ////double time_step_sec = bullet_environment->();
    //double fixed_sub_time_step_sec = bullet_environment->getBulletFixedTimeSubStepSec();
    ////double num_sub_steps = time_step_sec / fixed_sub_time_step_sec;
    //double max_sub_steps = bullet_environment->getBulletMaxSubSteps();

    this->dataMap["elapsed_simulation_time_sec"].push_back(elapsed_simulation_time_sec);
    this->dataMap["elapsed_user_time_sec"].push_back(elapsed_user_time_sec);
    ////this->dataMap["time_step_sec"].push_back(time_step_sec);
    //this->dataMap["fixed_sub_time_step_sec"].push_back(fixed_sub_time_step_sec);
    ////this->dataMap["num_sub_steps"].push_back(num_sub_steps);
    //this->dataMap["max_sub_steps"].push_back(max_sub_steps);
}

std::string simulator::LoggerTimeStepsBulletEnvironmentJson::getFilepath() const {
    return this->filepath;
}
