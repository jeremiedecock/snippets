/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"
#include "osg_environment.h"

#include "joints/point_to_point.h"

#include "object.h"

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

static double radius = 1.;
static double mass = 1.;
static double friction = 0.5;
static double rolling_friction = 0.;
static double restitution = 0.;

static Eigen::Vector3d initial_position;
static Eigen::Vector4d initial_angle;
static Eigen::Vector3d initial_velocity;
static Eigen::Vector3d initial_angular_velocity;
static Eigen::Vector3d initial_inertia;

static std::string initial_position_str_opt         = "0.,0.,10.";
static std::string initial_angle_str_opt            = "0.,0.,0.,1.";
static std::string initial_velocity_str_opt         = "1.,0.,0.";
static std::string initial_angular_velocity_str_opt = "0.,0.,0.";
static std::string initial_inertia_str_opt          = "0.,0.,0.";

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
        ("mass",             po::value<double>(&mass)->default_value(mass), "set the sphere mass (in kilograms). Expects a decimal number.")
        ("friction",         po::value<double>(&friction)->default_value(friction), "set the sphere and the ground friction value. Expects a decimal number (ideally between 0. and 1.). Best simulation results when friction is non-zero.")
        ("rolling_friction", po::value<double>(&rolling_friction)->default_value(rolling_friction), "set the sphere rolling friction value. Expects a decimal number (ideally between 0. and 1.).")
        ("restitution",      po::value<double>(&restitution)->default_value(restitution), "set the sphere and the ground restitution value. Expects a decimal number (ideally between 0. and 1.). Best simulation results using zero restitution.")
        ("radius",           po::value<double>(&radius)->default_value(radius), "set the sphere radius (in meters). Expects a decimal number.")
        ("position",         po::value<std::string>(&initial_position_str_opt)->default_value(initial_position_str_opt), "set the initial position vector of the sphere (in meters). Expects a vector of 3 decimal numbers separated with a comma and without space character (e.g. \"1.0,2.0,3.0\").")
        ("angle",            po::value<std::string>(&initial_angle_str_opt)->default_value(initial_angle_str_opt), "set the initial angle of the sphere using a quaternion representation. Expects a vector of 4 decimal numbers separated with a comma and without space character (e.g. \"1.0,2.0,3.0,4.0\").")
        ("velocity",         po::value<std::string>(&initial_velocity_str_opt)->default_value(initial_velocity_str_opt), "set the initial velocity vector of the sphere. Expects a vector of 3 decimal numbers separated with a comma and without space character (e.g. \"1.0,2.0,3.0\").")
        ("angular_velocity", po::value<std::string>(&initial_angular_velocity_str_opt)->default_value(initial_angular_velocity_str_opt), "set the initial angular velocity vector of the sphere. Expects a vector of 3 decimal numbers separated with a comma and without space character (e.g. \"1.0,2.0,3.0\").")
        ("inertia",          po::value<std::string>(&initial_inertia_str_opt)->default_value(initial_inertia_str_opt), "set the initial inertia vector of the sphere. Expects a vector of 3 decimal numbers separated with a comma and without space character (e.g. \"1.0,2.0,3.0\").")
    ;

    // Parse programm options (local and common)
    
    simulator::CommonOptionsParser options(argc, argv, local_options_desc);

    if(options.exit) {
        return options.exitValue;
    }

    // Assign some options value (vectors)
    
    initial_position = simulator::string_to_eigen_vector3(initial_position_str_opt);
    initial_angle = simulator::string_to_eigen_vector4(initial_angle_str_opt);
    initial_velocity = simulator::string_to_eigen_vector3(initial_velocity_str_opt);
    initial_angular_velocity = simulator::string_to_eigen_vector3(initial_angular_velocity_str_opt);
    initial_inertia = simulator::string_to_eigen_vector3(initial_inertia_str_opt);

    // Print options value

    if(options.verbose) {
        std::cout << "MASS: " << mass << "kg" << std::endl;
        std::cout << "FRICTION: " << friction << std::endl;
        std::cout << "ROLLING FRICTION: " << rolling_friction << std::endl;
        std::cout << "RESTITUTION: " << restitution << std::endl;
        std::cout << "RADIUS: " << radius << "m" << std::endl;
        std::cout << "INITIAL POSITION: " << simulator::eigen_vector_to_string(initial_position) << std::endl;
        std::cout << "INITIAL ANGLE: " << simulator::eigen_vector_to_string(initial_angle) << std::endl;
        std::cout << "INITIAL VELOCITY: " << simulator::eigen_vector_to_string(initial_velocity) << std::endl;
        std::cout << "INITIAL ANGULAR VELOCITY: " << simulator::eigen_vector_to_string(initial_angular_velocity) << std::endl;
        std::cout << "INITIAL INERTIA: " << simulator::eigen_vector_to_string(initial_inertia) << std::endl;
    }

    // Init Bullet ////////////////////////////////////////////////////////////

    // Pendulum object ////////////////

    // Pendulum parts
    simulator::Sphere sphere(radius, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass, friction, rolling_friction, restitution, "pendulum_sphere");

    std::set<simulator::Part *> pendulum_part_set;
    pendulum_part_set.insert(&sphere);

    // Pendulum joints
    Eigen::Vector3d pendulum_p2p_pivot(-5., 0., 0.);
    simulator::PointToPoint pendulum_p2p(&sphere, pendulum_p2p_pivot, "pendulum_point_to_point");

    std::set<simulator::Joint *> pendulum_joint_set;
    pendulum_joint_set.insert(&pendulum_p2p);

    // Pendulum object
    simulator::Object pendulum(pendulum_part_set, pendulum_joint_set, "pendulum");

    // Other parts ////////////////////
    
    // Ground
    simulator::Ground ground(friction, rolling_friction, restitution);

    // Bullet environment /////////////
    
    // Bullet object set
    std::set<simulator::Object *> bullet_object_set;
    bullet_object_set.insert(&pendulum);

    // Bullet part set
    std::set<simulator::Part *> bullet_part_set;
    bullet_part_set.insert(&ground);

    // Bullet environment
    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(bullet_object_set, bullet_part_set, options.timeStepDurationSec, options.tickDurationSec, options.maxTicksPerTimeStep, options.simulationDurationSec);

    // Init log ///////////////////////////////////////////////////////////////

    // Bullet time steps dat log
    simulator::LoggerTimeStepsBulletEnvironmentDat * p_logger_time_steps_bullet_environment_dat = new simulator::LoggerTimeStepsBulletEnvironmentDat();
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_dat);

    // Bullet time steps json log
    simulator::LoggerTimeStepsBulletEnvironmentJson * p_logger_time_steps_bullet_environment_json = new simulator::LoggerTimeStepsBulletEnvironmentJson();
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_json);

    // Parts time steps dat log
    simulator::LoggerTimeStepsPartsDat * p_logger_time_steps_parts_dat = new simulator::LoggerTimeStepsPartsDat(bullet_part_set);
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_dat);

    // Parts time steps json log
    simulator::LoggerTimeStepsPartsJson * p_logger_time_steps_parts_json = new simulator::LoggerTimeStepsPartsJson(bullet_part_set);
    bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_json);

    // Parts ticks dat log
    simulator::LoggerTicksPartsDat * p_logger_ticks_parts_dat = new simulator::LoggerTicksPartsDat(bullet_part_set);
    bullet_environment->attachTickObserver(p_logger_ticks_parts_dat);

    // Parts ticks json log
    simulator::LoggerTicksPartsJson * p_logger_ticks_parts_json = new simulator::LoggerTicksPartsJson(bullet_part_set);
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
