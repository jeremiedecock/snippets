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

botsim::LoggerTimeStepsBulletEnvironmentJson::LoggerTimeStepsBulletEnvironmentJson(std::string filepath) {
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
    this->dataMap["tick_duration_sec"] = std::vector<double>();
    //this->dataMap["num_ticks"] = std::vector<double>();
    this->dataMap["max_ticks_per_time_step"] = std::vector<double>();
}

botsim::LoggerTimeStepsBulletEnvironmentJson::~LoggerTimeStepsBulletEnvironmentJson() {
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

void botsim::LoggerTimeStepsBulletEnvironmentJson::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();
    double elapsed_user_time_sec = bullet_environment->getElapsedUserTimeSec();
    //double time_step_sec = bullet_environment->();
    double tick_duration_sec = bullet_environment->getBulletTickDurationSec();
    //double num_ticks = time_step_sec / tick_duration_sec;
    double max_ticks_per_time_step = bullet_environment->getBulletMaxTicksPerTimeStep();

    this->dataMap["elapsed_simulation_time_sec"].push_back(elapsed_simulation_time_sec);
    this->dataMap["elapsed_user_time_sec"].push_back(elapsed_user_time_sec);
    //this->dataMap["time_step_sec"].push_back(time_step_sec);
    this->dataMap["tick_duration_sec"].push_back(tick_duration_sec);
    //this->dataMap["num_ticks"].push_back(num_ticks);
    this->dataMap["max_ticks_per_time_step"].push_back(max_ticks_per_time_step);
}

std::string botsim::LoggerTimeStepsBulletEnvironmentJson::getFilepath() const {
    return this->filepath;
}
