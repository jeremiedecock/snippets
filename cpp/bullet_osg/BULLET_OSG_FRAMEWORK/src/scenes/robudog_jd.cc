/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "bullet_environment.h"
#include "osg_environment.h"

#include "actuator.h"
#include "actuators/motor.h"

#include "builtin_parts/dynamixel_ax12.h"
#include "builtin_objects/robudog_jd.h"

#include "controller.h"
#include "controllers/constant_signal.h"
#include "controllers/sinusoidal_signal.h"

#include "joint.h"
#include "joint_slots/hinge_slot.h"

#include "object.h"

#include "part.h"
#include "parts/ground.h"

#include "sensor.h"
#include "sensors/clock.h"

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

static double ground_friction = 0.5;
static double ground_rolling_friction = 0.;
static double ground_restitution = 0.;

/*
 * MAIN FUNCTION
 */

int main(int argc, char * argv[]) {

    // Parse program params ///////////////////////////////////////////////////

    po::options_description local_options_desc; // No local option...
    
    simulator::CommonOptionsParser options(argc, argv, local_options_desc);

    if(options.exit) {
        return options.exitValue;
    }

    // Init Bullet ////////////////////////////////////////////////////////////

    // Robudog object ////////////////

    simulator::Object * p_robudog = simulator::make_robudog_jd();
    
    // Other parts ////////////////////
    
    // Ground
    simulator::Ground * p_ground = new simulator::Ground(ground_friction, ground_rolling_friction, ground_restitution);
    
    // Controllers ////////////////////
    
    simulator::Clock * p_clock_sensor = new simulator::Clock(NULL, "clock");  // TODO: UGLY WORKAROUND !
    std::set<simulator::Sensor *> sensor_set;
    sensor_set.insert(p_clock_sensor);

    //simulator::ConstantSignal p_robudog_controller(robudog_actuator_set, sensor_set, 2.0, "robudog_controller");
    //simulator::SinusoidalSignal * p_robudog_controller = new simulator::SinusoidalSignal(p_robudog->getActuatorSet(), sensor_set, 4., 0.25, 3.14/2., "robudog_controller");

    // Bullet environment /////////////
    
    // Bullet object set
    std::set<simulator::Object *> bullet_object_set;
    bullet_object_set.insert(p_robudog);

    // Bullet part set
    std::set<simulator::Part *> bullet_part_set;
    bullet_part_set.insert(p_ground);
    
    // Controller set
    std::set<simulator::Controller *> controller_set;
    //controller_set.insert(p_robudog_controller);

    // Bullet environment
    simulator::BulletEnvironment * p_bullet_environment = new simulator::BulletEnvironment(bullet_object_set, bullet_part_set, controller_set, options.timeStepDurationSec, options.tickDurationSec, options.maxTicksPerTimeStep, options.simulationDurationSec);

    
    p_clock_sensor->bulletEnvironment = p_bullet_environment;  // TODO: UGLY WORKAROUND !

    // Init log ///////////////////////////////////////////////////////////////

    // Bullet time steps dat log
    simulator::LoggerTimeStepsBulletEnvironmentDat * p_logger_time_steps_bullet_environment_dat = new simulator::LoggerTimeStepsBulletEnvironmentDat();
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_dat);

    // Bullet time steps json log
    simulator::LoggerTimeStepsBulletEnvironmentJson * p_logger_time_steps_bullet_environment_json = new simulator::LoggerTimeStepsBulletEnvironmentJson();
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_bullet_environment_json);

    // Parts time steps dat log
    simulator::LoggerTimeStepsPartsDat * p_logger_time_steps_parts_dat = new simulator::LoggerTimeStepsPartsDat(p_robudog->getPartSet());
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_dat);

    // Parts time steps json log
    simulator::LoggerTimeStepsPartsJson * p_logger_time_steps_parts_json = new simulator::LoggerTimeStepsPartsJson(p_robudog->getPartSet());
    p_bullet_environment->attachTimeStepObserver(p_logger_time_steps_parts_json);

    // Parts ticks dat log
    simulator::LoggerTicksPartsDat * p_logger_ticks_parts_dat = new simulator::LoggerTicksPartsDat(p_robudog->getPartSet());
    p_bullet_environment->attachTickObserver(p_logger_ticks_parts_dat);

    // Parts ticks json log
    simulator::LoggerTicksPartsJson * p_logger_ticks_parts_json = new simulator::LoggerTicksPartsJson(p_robudog->getPartSet());
    p_bullet_environment->attachTickObserver(p_logger_ticks_parts_json);


    // Run the simulation /////////////////////////////////////////////////////

    simulator::OSGEnvironment * osg_environment = NULL;

    if(options.useHeadLessMode) {
        // Run Bullet
        p_bullet_environment->run();
    } else {
        // Init OSG
        osg_environment = new simulator::OSGEnvironment(p_bullet_environment, options.useFullScreenMode);

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
    delete p_bullet_environment;

    if(!options.useHeadLessMode) {
        std::cout << "Delete OSG environment." << std::endl;
        delete osg_environment;
    }

    std::cout << "Bye." << std::endl;

    return 0;
}
