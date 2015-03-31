/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "parts/sphere.h"
#include "parts/ground.h"
#include "bullet_environment.h"
#include "osg_environment.h"
#include "part.h"
#include "tools/logger_ticks_parts_dat.h"
#include "tools/logger_ticks_parts_json.h"
#include "tools/logger_time_steps_parts_dat.h"
#include "tools/logger_time_steps_parts_json.h"
#include "tools/tools.h"

#include <set>
#include <iostream>

#include <Eigen/Dense>


int main(int, char **) {

    // Init Bullet //////////////////////////////////////////////////////////////////////

    std::set<simulator::Part *> parts_set;

    double initial_radius = 1.;
    Eigen::Vector3d initial_position = Eigen::Vector3d(0., 0., 50.);
    Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
    Eigen::Vector3d initial_velocity = Eigen::Vector3d(1., 0., 0.);
    Eigen::Vector3d initial_angular_velocity = Eigen::Vector3d(0., 0., 0.);
    Eigen::Vector3d initial_inertia = Eigen::Vector3d(0., 0., 0.);
    double mass = 1.;

    simulator::Sphere sphere = simulator::Sphere(initial_radius, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass);
    simulator::Ground ground;

    parts_set.insert(&sphere);
    parts_set.insert(&ground);

    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(parts_set);

    // Init log /////////////////////////////////////////////////////////////////////////

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

    // Init OSG /////////////////////////////////////////////////////////////////////////

    simulator::OSGEnvironment * osg_environment = new simulator::OSGEnvironment(bullet_environment);

    // Run the simulation ///////////////////////////////////////////////////////////////
    
    osg_environment->run();

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    delete p_logger_time_steps_parts_dat;
    delete p_logger_time_steps_parts_json;
    delete p_logger_ticks_parts_dat;
    delete p_logger_ticks_parts_json;

    std::cout << "Delete Bullet environment." << std::endl;
    delete bullet_environment;
    std::cout << "Delete OSG environment." << std::endl;
    delete osg_environment;
    std::cout << "Bye." << std::endl;

    return 0;
}
