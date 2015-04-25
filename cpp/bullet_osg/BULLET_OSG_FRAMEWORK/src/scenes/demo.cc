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

static double cube_size = 0.9;
static double height = 10.;
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

    // Init Bullet //////////////////////////////////////////////////////////////////////
    
    // Bullet object set
    std::set<simulator::Object *> bullet_object_set;

    // Bullet part set
    std::set<simulator::Part *> bullet_part_set;

    bullet_part_set.insert(new simulator::Ground());

    for(int x_index=0 ; x_index <= 3 ; x_index++) {
        for(int y_index=0 ; y_index <= 3 ; y_index++) {
            for(int z_index=0 ; z_index <= 3 ; z_index++) {
                Eigen::Vector3d initial_dimension = Eigen::Vector3d(cube_size, cube_size, cube_size);
                Eigen::Vector3d initial_position = Eigen::Vector3d(x_index, y_index, z_index + height);

                simulator::Part * p_part = new simulator::Box(initial_dimension, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass);
                bullet_part_set.insert(p_part);
            }
        }
    }
    
    // Controller set
    std::set<simulator::Controller *> controller_set;

    // Bullet environment
    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(bullet_object_set, bullet_part_set, controller_set, options.timeStepDurationSec, options.tickDurationSec, options.maxTicksPerTimeStep, options.simulationDurationSec);

    // Run the simulation ///////////////////////////////////////////////////////////////

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

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    std::cout << "Delete Bullet environment." << std::endl;
    delete bullet_environment;

    if(!options.useHeadLessMode) {
        std::cout << "Delete OSG environment." << std::endl;
        delete osg_environment;
    }

    std::cout << "Bye." << std::endl;

    return 0;
}
