/* 
 * Bullet OSG Framework.
 * Common options parser module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "common_options_parser.h"
#include "tools/tools.h"

#include <fstream>
#include <iostream>


/*
 * LOCAL OPTIONS
 */

static const bool DEFAULT_USE_FULL_SCREEN_MODE = false;
static const bool DEFAULT_USE_HEAD_LESS_MODE = false;

static const double DEFAULT_TIME_STEP_DURATION_SEC = -1.0;
static const double DEFAULT_TICK_DURATION_SEC = 0.003;
static const int DEFAULT_MAX_TICKS_PER_TIME_STEP = 1000;

static const double DEFAULT_SIMULATION_DURATION_SEC = -1.0;

static const std::string DEFAULT_CONFIG_FILE = "";

static const bool DEFAULT_USE_VERBOSE_MODE = false;


/**
 *
 */
botsim::CommonOptionsParser::CommonOptionsParser(int argc,
                                                    char * argv[],
                                                    const po::options_description & local_options_desc) {

    // Set some default values
    
    this->exit = false;
    this->exitValue = 0;

    /*
     * Declare the group of common options that are allowed on command line
     * and config file.
     */

    /* 
     * Validates bool value
     * (see $(BOOST_ROOT)/libs/program_options/src/value_semantic.cpp):
     *
     * Any of "1", "true", "yes", "on" will be converted to "1".
     * Any of "0", "false", "no", "off" will be converted to "0".
     * Case is ignored. The 'xs' vector can either be empty, in which
     * case the value is 'true', or can contain explicit value.
     */

    po::options_description common_options_desc;
    common_options_desc.add_options()
        ("help,h", "produce help message")
        ("full_screen,F",                 po::value<bool>(&(this->useFullScreenMode))->default_value(DEFAULT_USE_FULL_SCREEN_MODE),          "set full screen mode. Expects \"on\" (1) or \"off\" (0).")
        ("head_less,q",                   po::value<bool>(&(this->useHeadLessMode))->default_value(DEFAULT_USE_HEAD_LESS_MODE),              "set head less mode. Expects \"on\" (1) or \"off\" (0).")
        ("time_step_duration_sec,T",      po::value<double>(&(this->timeStepDurationSec))->default_value(DEFAULT_TIME_STEP_DURATION_SEC),    "setup time step duration (in seconds). Expects a decimal number.")
        ("tick_duration_sec,t",           po::value<double>(&(this->tickDurationSec))->default_value(DEFAULT_TICK_DURATION_SEC),             "setup tick duration (in seconds). Expects a decimal number.")
        ("max_ticks_per_time_step,m",     po::value<int>(&(this->maxTicksPerTimeStep))->default_value(DEFAULT_MAX_TICKS_PER_TIME_STEP),      "set the maximum number of ticks per time step. Expects an integer number.")
        ("simulation_duration_sec,d",     po::value<double>(&(this->simulationDurationSec))->default_value(DEFAULT_SIMULATION_DURATION_SEC), "setup simulation duration (in seconds). Expects a decimal number.")
        ("config,c",                      po::value<std::string>(&(this->configFile))->default_value(DEFAULT_CONFIG_FILE),                   "name of the configuration file.")
        ("verbose,v",                     po::value<bool>(&(this->verbose))->default_value(DEFAULT_USE_VERBOSE_MODE),                        "set the verbose mode. Expects the value \"on\" (1) or \"off\" (0).")
//        ("random_seed",                   po::value<time_t>(),      "set random seed value (if seed!=0 then use a deterministic pseudo random numbers sequence).")
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

    //po::variables_map this->variableMap;

    po::store(po::parse_command_line(argc, argv, local_and_global_options_desc), this->variableMap);
    po::notify(this->variableMap);

    /*
     * Parse config file
     */

    if(this->variableMap.count("config")) {
        this->configFile = this->variableMap["config"].as<std::string>();
    }

    if(this->configFile != "") {
        std::ifstream ifs(this->configFile.c_str());
        if(!ifs) {
            std::cout << "Can not open config file: " << this->configFile << std::endl;

            this->exit = true;
            this->exitValue = 1;
            //return;
        } else {
            po::store(po::parse_config_file(ifs, local_and_global_options_desc), this->variableMap);
            po::notify(this->variableMap);
        }
    }

    /*
     * Assign options value
     */

    // Help
    if(this->variableMap.count("help") && !this->exit) {
        std::cout << "This is a snippet using botsim.org, a robotic simulation framework." << std::endl << std::endl;
        std::cout <<   local_and_global_options_desc << std::endl;

        this->exit = true;
        this->exitValue = 0;
        //return;
    }

//    // Setup full screen mode
//    if(this->variableMap.count("full_screen")) {
//        use_full_screen_mode = this->variableMap["full_screen"].as<bool>();
//    }
//
//    // Setup head less mode
//    if(this->variableMap.count("head_less")) {
//        use_head_less_mode = this->variableMap["head_less"].as<bool>();
//    }
//
//    // Setup ticks duration (in seconds)
//    if(this->variableMap.count("tick_duration_sec")) {
//        tick_duration_sec = this->variableMap["tick_duration_sec"].as<double>();
//    }
//
//    // Setup time steps duration (in seconds)
//    if(this->variableMap.count("time_step_duration_sec")) {
//        time_step_duration_sec = this->variableMap["time_step_duration_sec"].as<double>();
//    }
//
//    // Setup maximum ticks per time step
//    if(this->variableMap.count("max_ticks_per_time_step")) {
//        max_ticks_per_time_step = this->variableMap["max_ticks_per_time_step"].as<int>();
//    }
//
//    // Setup simulation duration (in seconds)
//    if(this->variableMap.count("simulation_duration_sec")) {
//        simulation_duration_sec = this->variableMap["simulation_duration_sec"].as<double>();
//    }
    
    /*
     * Print options value
     */

    if(this->verbose && !this->exit) {
        if(this->useFullScreenMode) {
            std::cout << "FULL SCREEN MODE ON" << std::endl;
        } else {
            std::cout << "FULL SCREEN MODE OFF" << std::endl;
        }

        if(this->useHeadLessMode) {
            std::cout << "HEAD LESS MODE ON" << std::endl;
        } else {
            std::cout << "HEAD LESS MODE OFF" << std::endl;
        }

        std::cout << "TICKS DURATION: " << this->tickDurationSec << "s" << std::endl;
        std::cout << "TIME STEPS DURATION: " << this->timeStepDurationSec << "s" << std::endl;
        std::cout << "MAX TICKS PER TIME STEP: " << this->maxTicksPerTimeStep << std::endl;
        std::cout << "SIMULATION DURATION: " << this->simulationDurationSec << "s" << std::endl;
    }
}
