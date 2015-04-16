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
#include "tools/logger_ticks_parts_dat.h"
#include "tools/logger_ticks_parts_json.h"
#include "tools/logger_time_steps_parts_dat.h"
#include "tools/logger_time_steps_parts_json.h"
#include "tools/logger_time_steps_bullet_environment_dat.h"
#include "tools/logger_time_steps_bullet_environment_json.h"
#include "tools/tools.h"

#include <boost/program_options.hpp>

#include <iostream>
#include <set>
#include <string>

#include <Eigen/Dense>

namespace po = boost::program_options;


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
 * PARSE PROGRAMME OPTIONS FUNCTION
 */

// COMMON OPTIONS

static bool use_full_screen_mode = false;
static bool use_head_less_mode = false;

static double time_step_duration_sec = -1.0;
static double tick_duration_sec = 0.003;
static int max_ticks_per_time_step = 1000;

static double simulation_duration_sec = -1.0;

static std::string config_file = "";

void parse_programm_options(int argc, char * argv[], const po::options_description & local_options_desc, bool verbose, bool * p_exit, int * p_exit_value) {

    /*
     * Declare the group of common options that are allowed on command line
     * and config file.
     */

    po::options_description common_options_desc;
    common_options_desc.add_options()
        ("help,h", "produce help message")
        ("full_screen,F",                 po::value<bool>(),        (std::string("set full screen mode. Take 0 or 1. Default is: ") +                                     simulator::to_string(use_full_screen_mode)).c_str())
        ("head_less,q",                   po::value<bool>(),        (std::string("set head less mode. Take 0 or 1. Default is: ") +                                       simulator::to_string(use_head_less_mode)).c_str())
        ("tick_duration_sec,t",           po::value<double>(),      (std::string("setup tick duration (in seconds). Take a real number. Default is: ") +                  simulator::to_string(tick_duration_sec)).c_str())
        ("time_step_duration_sec,T",      po::value<double>(),      (std::string("setup time step duration (in seconds). Take a real number. Default is: ") +             simulator::to_string(time_step_duration_sec)).c_str())
        ("max_ticks_per_time_step,m",     po::value<int>(),         (std::string("set the maximum number of ticks per time step. Take an integer number. Default is: ") + simulator::to_string(max_ticks_per_time_step)).c_str())
        ("simulation_duration_sec,d",     po::value<double>(),      (std::string("setup simulation duration (in seconds). Take a real number. Default is: ") +            simulator::to_string(simulation_duration_sec)).c_str())
        ("config,c",                      po::value<std::string>(), (std::string("name of the configuration file. Default is: \"") +                                      simulator::to_string(config_file) + std::string("\"")).c_str())
        //        ("random_seed",                   po::value<time_t>(),      (std::string("set random seed value (if seed!=0 then use a deterministic pseudo random numbers sequence). Default is: ") + to_string(seed)).c_str())
        ;

    /*
     * Declare the group of local and common options that are allowed on
     * command line and config file.
     */

    po::options_description local_and_global_options_desc("Allowed options");
    local_and_global_options_desc.add(common_options_desc).add(local_options_desc);

    /*
     * Parse commandline options
     */

    po::variables_map vm;

    po::store(po::parse_command_line(argc, argv, local_and_global_options_desc), vm);
    po::notify(vm);

    /*
     * Parse config file
     */

    if(vm.count("config")) {
        config_file = vm["config"].as<std::string>();
    }

    if(config_file != "") {
        std::ifstream ifs(config_file.c_str());
        if(!ifs) {
            std::cout << "Can not open config file: " << config_file << std::endl;

            *p_exit = true;
            *p_exit_value = 1;
            return;
        } else {
            po::store(po::parse_config_file(ifs, local_and_global_options_desc), vm);
            po::notify(vm);
        }
    }

    /*
     * Assign options value
     */

    // Help
    if(vm.count("help")) {
        std::cout << "This is a snippet using botsim.org, a robotic simulation framework." << std::endl << std::endl;
        std::cout <<   local_and_global_options_desc << std::endl;

        *p_exit = true;
        *p_exit_value = 0;
        return;
    }

    // Setup full screen mode
    if(vm.count("full_screen")) {
        use_full_screen_mode = vm["full_screen"].as<bool>();
    }

    // Setup head less mode
    if(vm.count("head_less")) {
        use_head_less_mode = vm["head_less"].as<bool>();
    }

    // Setup ticks duration (in seconds)
    if(vm.count("tick_duration_sec")) {
        tick_duration_sec = vm["tick_duration_sec"].as<double>();
    }

    // Setup time steps duration (in seconds)
    if(vm.count("time_step_duration_sec")) {
        time_step_duration_sec = vm["time_step_duration_sec"].as<double>();
    }

    // Setup maximum ticks per time step
    if(vm.count("max_ticks_per_time_step")) {
        max_ticks_per_time_step = vm["max_ticks_per_time_step"].as<int>();
    }

    // Setup simulation duration (in seconds)
    if(vm.count("simulation_duration_sec")) {
        simulation_duration_sec = vm["simulation_duration_sec"].as<double>();
    }
    
    /*
     * Print options value
     */

    if(verbose) {
        if(use_full_screen_mode) {
            std::cout << "FULL SCREEN MODE ON" << std::endl;
        } else {
            std::cout << "FULL SCREEN MODE OFF" << std::endl;
        }

        if(use_head_less_mode) {
            std::cout << "HEAD LESS MODE ON" << std::endl;
        } else {
            std::cout << "HEAD LESS MODE OFF" << std::endl;
        }

        std::cout << "TICKS DURATION: " << tick_duration_sec << "s" << std::endl;
        std::cout << "TIME STEPS DURATION: " << time_step_duration_sec << "s" << std::endl;
        std::cout << "MAX TICKS PER TIME STEP: " << max_ticks_per_time_step << std::endl;
        std::cout << "SIMULATION DURATION: " << simulation_duration_sec << "s" << std::endl;
    }
}




/*
 * MAIN FUNCTION
 */

int main(int argc, char * argv[]) {

    // Parse program params ///////////////////////////////////////////////////

    // Declare the group of local options that are allowed on command line and config file.

    po::options_description local_options_desc;
    local_options_desc.add_options()
        ("mass",     po::value<double>(&mass),         (std::string("set the sphere mass. Default is: ") +              simulator::to_string(mass)).c_str())
    ;

    // Parse programm options (local and common).
    
    bool verbose = false;
    bool exit = false;
    int  exit_value = 0;

    parse_programm_options(argc, argv, local_options_desc, verbose, &exit, &exit_value);

    if(exit) {
        return exit_value;
    }

    // Print options value

    std::cout << "MASS: " << mass << "kg" << std::endl;

    // Init Bullet ////////////////////////////////////////////////////////////

    std::set<simulator::Part *> parts_set;

    simulator::Sphere sphere = simulator::Sphere(initial_radius, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass);
    simulator::Ground ground;

    parts_set.insert(&sphere);
    parts_set.insert(&ground);

    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(parts_set, time_step_duration_sec, tick_duration_sec, max_ticks_per_time_step, simulation_duration_sec);

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

    if(use_head_less_mode) {
        // Run Bullet
        bullet_environment->run();
    } else {
        // Init OSG
        osg_environment = new simulator::OSGEnvironment(bullet_environment, use_full_screen_mode);

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

    if(!use_head_less_mode) {
        std::cout << "Delete OSG environment." << std::endl;
        delete osg_environment;
    }

    std::cout << "Bye." << std::endl;

    return 0;
}
