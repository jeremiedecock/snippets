/* 
 * Bullet OSG Framework.
 * Bullet environment logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "logger_time_steps_bullet_environment_dat.h"
#include "tools/tools.h"

#include <iostream>

const std::string DEFAULT_FILE_PATH = "time_steps_bullet_environment.dat"; // TODO ?

botsim::LoggerTimeStepsBulletEnvironmentDat::LoggerTimeStepsBulletEnvironmentDat(std::string filepath) {
    // Set filepath
    if(filepath == "") {
        this->filepath = DEFAULT_FILE_PATH;
    } else {
        this->filepath = filepath;
    }
    
    // Open the log file
    std::cout << "Open " << this->filepath << std::endl;
    this->ofs = new std::ofstream(this->filepath.c_str());
    
    // Write the header
    (* this->ofs) << "#elapsed_simulation_time_sec  ";
    (* this->ofs) << "elapsed_user_time_sec  ";
    //(* this->ofs) << "time_step_sec  ";
    (* this->ofs) << "tick_duration_sec  ";
    //(* this->ofs) << "num_ticks  ";
    (* this->ofs) << "max_ticks_per_time_step  ";
    (* this->ofs) << std::endl;
}

botsim::LoggerTimeStepsBulletEnvironmentDat::~LoggerTimeStepsBulletEnvironmentDat() {
    // Open the log file
    std::cout << "Close " << this->filepath << std::endl;
    this->ofs->flush();
    this->ofs->close();

    // Destroy dynamic objects
    delete this->ofs;
}

void botsim::LoggerTimeStepsBulletEnvironmentDat::update(BulletEnvironment * bullet_environment) {
    double elapsed_simulation_time_sec = bullet_environment->getElapsedSimulationTimeSec();
    double elapsed_user_time_sec = bullet_environment->getElapsedUserTimeSec();
    //double time_step_sec = bullet_environment->();
    double tick_duration_sec = bullet_environment->getBulletTickDurationSec();
    //double num_ticks = time_step_sec / tick_duration_sec;
    double max_ticks_per_time_step = bullet_environment->getBulletMaxTicksPerTimeStep();
    
    (* this->ofs) << elapsed_simulation_time_sec << " ";
    (* this->ofs) << elapsed_user_time_sec << " ";
    //(* this->ofs) << time_step_sec << " ";
    (* this->ofs) << tick_duration_sec << " ";
    //(* this->ofs) << num_ticks << " ";
    (* this->ofs) << max_ticks_per_time_step << " ";
    (* this->ofs) << std::endl;
}

std::string botsim::LoggerTimeStepsBulletEnvironmentDat::getFilepath() const {
    return this->filepath;
}
