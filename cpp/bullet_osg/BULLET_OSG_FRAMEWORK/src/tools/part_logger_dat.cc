/* 
 * Bullet OSG Framework.
 * Part logger module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "part_logger_dat.h"

#include <iostream>

const std::string DEFAULT_FILE_PATH = "log.dat"; // TODO ?

simulator::PartLoggerDat::PartLoggerDat(std::set<simulator::Part *> observed_parts_set, std::string filepath) {
    //// Set logged parts
    //std::set<Part *>::iterator it;
    //for(it = observed_parts_set.begin() ; it != observed_parts_set.end() ; it++) {
    //    this->attach(*it);
    //}
    this->observedPartSet = observed_parts_set;

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
    (* this->ofs) << "#foo" << std::endl; // TODO
}

simulator::PartLoggerDat::~PartLoggerDat() {
    // Close the log file
    std::cout << "Close " << this->filepath << std::endl;
    this->ofs->flush();
    this->ofs->close();

    // Destroy dynamic objects
    delete this->ofs;
}

void simulator::PartLoggerDat::update(BulletEnvironment * bullet_environment) {
    std::set<Part *>::iterator it;
    for(it = this->observedPartSet.begin() ; it != this->observedPartSet.end() ; it++) {
        // TODO: find ... if ...
        (* this->ofs) << (*it)->getPosition() << std::endl;
    }
}

std::string simulator::PartLoggerDat::getFilepath() const {
    return this->filepath;
}
