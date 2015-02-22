/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "box.h"
#include "bullet_environment.h"
#include "ground.h"
#include "osg_environment.h"
#include "part.h"
#include "tools.h"

#include <vector>
#include <iostream>

#include <Eigen/Dense>


int main(int, char **) {

    // Init Bullet //////////////////////////////////////////////////////////////////////

    std::vector<simulator::Part *> * objects_vec = new std::vector<simulator::Part *>;
    objects_vec->push_back(new simulator::Ground());
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));

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
