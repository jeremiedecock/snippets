/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"
#include "osg_environment.h"

#include "part.h"
#include "parts/sphere.h"
#include "parts/ground.h"

#include "tools/common_options_parser.h"
#include "tools/logger_ticks_parts_dat.h"
#include "tools/logger_ticks_parts_json.h"
#include "tools/logger_time_steps_parts_dat.h"
#include "tools/logger_time_steps_parts_json.h"
#include "tools/logger_time_steps_bullet_environment_dat.h"
#include "tools/logger_time_steps_bullet_environment_json.h"
#include "tools/tools.h"

#include <boost/program_options.hpp>
namespace po = boost::program_options;

#include <iostream>
#include <set>
#include <string>

#include <Eigen/Dense>


/*
 * LOCAL OPTIONS
 */

static double initial_radius = 1.;
static Eigen::Vector3d initial_position = Eigen::Vector3d(0., 0., 50.);
static Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
static Eigen::Vector3d initial_velocity = Eigen::Vector3d(1., 0., 0.);
static Eigen::Vector3d initial_angular_velocity = Eigen::Vector3d(0., 0., 0.);
static Eigen::Vector3d initial_inertia = Eigen::Vector3d(0., 0., 0.);
static double mass = 1.;


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
    local_options_desc.add_options()
        ("mass",     po::value<double>(&mass)->default_value(mass), "set the sphere mass (in kilogram). Expects a decimal number.")
    ;

    // Parse programm options (local and common)
    
    simulator::CommonOptionsParser options(argc, argv, local_options_desc);

    if(options.exit) {
        return options.exitValue;
    }

    // Print options value

    if(options.verbose) {
        std::cout << "MASS: " << mass << "kg" << std::endl;
    }

    // Init Bullet ////////////////////////////////////////////////////////////

    std::set<simulator::Part *> parts_set;

    simulator::Sphere sphere = simulator::Sphere(initial_radius, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass);
    simulator::Ground ground;

    parts_set.insert(&sphere);
    parts_set.insert(&ground);

    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(parts_set, options.timeStepDurationSec, options.tickDurationSec, options.maxTicksPerTimeStep, options.simulationDurationSec);

    // Init log ///////////////////////////////////////////////////////////////

    // Bullet time steps dat log
    simulator::LoggerTimeStepsBulletEnvironmentDat * p_logger_time_steps_bullet_environment_dat = new simulator::LoggerTimeStepsBulletEnvironmentDat();
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_dat);

    // Bullet time steps json log
    simulator::LoggerTimeStepsBulletEnvironmentJson * p_logger_time_steps_bullet_environment_json = new simulator::LoggerTimeStepsBulletEnvironmentJson();
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_json);

    // Parts time steps dat log
    simulator::LoggerTimeStepsPartsDat * p_logger_time_steps_parts_dat = new simulator::LoggerTimeStepsPartsDat(parts_set);
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_dat);

    // Parts time steps json log
    simulator::LoggerTimeStepsPartsJson * p_logger_time_steps_parts_json = new simulator::LoggerTimeStepsPartsJson(parts_set);
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_json);

    // Parts ticks dat log
    simulator::LoggerTicksPartsDat * p_logger_ticks_parts_dat = new simulator::LoggerTicksPartsDat(parts_set);
    bullet_environment->attachTickObserver(p_logger_ticks_parts_dat);

    // Parts ticks json log
    simulator::LoggerTicksPartsJson * p_logger_ticks_parts_json = new simulator::LoggerTicksPartsJson(parts_set);
    bullet_environment->attachTickObserver(p_logger_ticks_parts_json);


    // Run the simulation /////////////////////////////////////////////////////

    simulator::OSGEnvironment * osg_environment = NULL;

    if(options.useHeadLessMode) {
        // Run Bullet
        bullet_environment->run();
    } else {
        // Init OSG
        osg_environment = new simulator::OSGEnvironment(bullet_environment, options.useFullScreenMode);

        // Run OSG
        osg_environment->run();
    }

    // Clean Bullet ///////////////////////////////////////////////////////////

    delete p_logger_time_steps_bullet_environment_dat;
    delete p_logger_time_steps_bullet_environment_json;
    delete p_logger_time_steps_parts_dat;
    delete p_logger_time_steps_parts_json;
    delete p_logger_ticks_parts_dat;
    delete p_logger_ticks_parts_json;

    std::cout << "Delete Bullet environment." << std::endl;
    delete bullet_environment;

    if(!options.useHeadLessMode) {
        std::cout << "Delete OSG environment." << std::endl;
        delete osg_environment;
    }

    std::cout << "Bye." << std::endl;

    return 0;
}
