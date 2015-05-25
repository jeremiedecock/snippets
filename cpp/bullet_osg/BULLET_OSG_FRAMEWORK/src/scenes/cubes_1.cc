/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"
#include "osg_environment.h"

#include "controller.h"

#include "object.h"

#include "part.h"
#include "parts/box.h"
#include "parts/ground.h"

#include "tools/common_options_parser.h"
#include "tools/logger_ticks_parts_dat.h"
#include "tools/logger_ticks_parts_json.h"
#include "tools/logger_time_steps_parts_dat.h"
#include "tools/logger_time_steps_parts_json.h"
#include "tools/tools.h"

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include <iostream>
#include <set>
#include <string>

#include <Eigen/Dense>


/*
 * MAIN FUNCTION
 */

int main(int argc, char * argv[]) {

    // Parse program params ///////////////////////////////////////////////////

    // Declare the group of local options that are allowed on command line and config file

    /* 
     * Validates bool value
     * (see $(BOOST_ROOT)/libs/program_options/src/value_semantic.cpp):
     *
     * Any of "1", "true", "yes", "on" will be converted to "1".
     * Any of "0", "false", "no", "off" will be converted to "0".
     * Case is ignored. The 'xs' vector can either be empty, in which
     * case the value is 'true', or can contain explicit value.
     */

    po::options_description local_options_desc;

    // Parse programm options (local and common)
    
    simulator::CommonOptionsParser options(argc, argv, local_options_desc);

    if(options.exit) {
        return options.exitValue;
    }

    // Init Bullet //////////////////////////////////////////////////////////////////////

    simulator::Box * p_box1 = new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Box * p_box2 = new simulator::Box(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Box * p_box3 = new simulator::Box(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.);
    simulator::Box * p_box4 = new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Ground * p_ground = new simulator::Ground();
    
    // Bullet object set
    std::set<simulator::Object *> bullet_object_set;

    // Bullet part set
    std::set<simulator::Part *> bullet_part_set;
    bullet_part_set.insert(p_ground);
    bullet_part_set.insert(p_box1);
    bullet_part_set.insert(p_box2);
    bullet_part_set.insert(p_box3);
    bullet_part_set.insert(p_box4);
    
    // Controller set
    std::set<simulator::Controller *> controller_set;

    // Bullet environment
    simulator::BulletEnvironment * p_bullet_environment = new simulator::BulletEnvironment(bullet_object_set, bullet_part_set, controller_set, options.timeStepDurationSec, options.tickDurationSec, options.maxTicksPerTimeStep, options.simulationDurationSec);

    // Init log /////////////////////////////////////////////////////////////////////////

    // Parts time steps dat log
    simulator::LoggerTimeStepsPartsDat * p_logger_time_steps_parts_dat = new simulator::LoggerTimeStepsPartsDat(bullet_part_set);
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_dat);

    // Parts time steps json log
    simulator::LoggerTimeStepsPartsJson * p_logger_time_steps_parts_json = new simulator::LoggerTimeStepsPartsJson(bullet_part_set);
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_json);

    // Parts ticks dat log
    simulator::LoggerTicksPartsDat * p_logger_ticks_parts_dat = new simulator::LoggerTicksPartsDat(bullet_part_set);
    p_bullet_environment->attachTickObserver(p_logger_ticks_parts_dat);

    // Parts ticks json log
    simulator::LoggerTicksPartsJson * p_logger_ticks_parts_json = new simulator::LoggerTicksPartsJson(bullet_part_set);
    p_bullet_environment->attachTickObserver(p_logger_ticks_parts_json);


    // Run the simulation ///////////////////////////////////////////////////////////////
    
    simulator::OSGEnvironment * p_osg_environment = NULL;

    if(options.useHeadLessMode) {
        // Run Bullet
        p_bullet_environment->run();
    } else {
        // Init OSG
        p_osg_environment = new simulator::OSGEnvironment(p_bullet_environment, options.useFullScreenMode);

        // Run OSG
        p_osg_environment->run();
    }

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    delete p_logger_time_steps_parts_dat;
    delete p_logger_time_steps_parts_json;
    delete p_logger_ticks_parts_dat;
    delete p_logger_ticks_parts_json;

    std::cout << "Delete Bullet environment." << std::endl;
    delete p_bullet_environment;
    //delete p_box1;
    //delete p_box2;
    //delete p_box3;
    //delete p_box4;
    //delete p_ground;

    if(!options.useHeadLessMode) {
        std::cout << "Delete OSG environment." << std::endl;
        delete p_osg_environment;
    }

    std::cout << "Bye." << std::endl;

    return 0;
}
