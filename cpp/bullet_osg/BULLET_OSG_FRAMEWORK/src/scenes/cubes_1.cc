/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "parts/box.h"
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

    simulator::Box box1(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Box box2(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Box box3(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.);
    simulator::Box box4(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.);
    simulator::Ground ground;

    parts_set.insert(&ground);
    parts_set.insert(&box1);
    parts_set.insert(&box2);
    parts_set.insert(&box3);
    parts_set.insert(&box4);

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

    delete bullet_environment;
    delete osg_environment;

    return 0;
}
