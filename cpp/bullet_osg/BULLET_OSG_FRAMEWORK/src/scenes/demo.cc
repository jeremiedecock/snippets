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
#include "tools/tools.h"

#include <vector>
#include <iostream>

#include <Eigen/Dense>


int main(int, char **) {

    // Init Bullet //////////////////////////////////////////////////////////////////////

    std::vector<simulator::Part *> * objects_vec = new std::vector<simulator::Part *>;

    objects_vec->push_back(new simulator::Ground());

    double cube_size = 0.9;

    for(int x_index=0 ; x_index <= 3 ; x_index++) {
        for(int y_index=0 ; y_index <= 3 ; y_index++) {
            for(int z_index=0 ; z_index <= 3 ; z_index++) {
                Eigen::Vector3d initial_dimension = Eigen::Vector3d(cube_size, cube_size, cube_size);
                Eigen::Vector3d initial_position = Eigen::Vector3d(x_index, y_index, z_index + 10.);
                Eigen::Vector4d initial_angle = Eigen::Vector4d(0., 0., 0., 1.);
                Eigen::Vector3d initial_velocity = Eigen::Vector3d(0., 0., 0.);
                Eigen::Vector3d initial_angular_velocity = Eigen::Vector3d(0., 0., 0.);
                Eigen::Vector3d initial_inertia = Eigen::Vector3d(0., 0., 0.);
                double mass = 1.;

                simulator::Part * p_part = new simulator::Box(initial_dimension, initial_position, initial_angle, initial_velocity, initial_angular_velocity, initial_inertia, mass);
                objects_vec->push_back(p_part);
            }
        }
    }

    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(objects_vec);

    // Init OSG /////////////////////////////////////////////////////////////////////////

    simulator::OSGEnvironment * osg_environment = new simulator::OSGEnvironment(bullet_environment, objects_vec);

    // Run the simulation ///////////////////////////////////////////////////////////////
    
    osg_environment->run();

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    delete bullet_environment;
    delete osg_environment;
    // TODO: delete object_vec and its contents

    return 0;
}
