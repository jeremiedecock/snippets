/* 
 * Bullet OSG Framework.
 * The bullet environment module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BULLET_ENVIRONMENT_H
#define BULLET_ENVIRONMENT_H

#include "part.h"

#include <vector>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class BulletEnvironment {

        // TODO: cette classe devrait être un singleton ?!

        private:
            btDiscreteDynamicsWorld * dynamicsWorld;
            btDbvtBroadphase * broadphase;
            btDefaultCollisionConfiguration * collisionConfiguration;
            btCollisionDispatcher * collisionDispatcher;
            btSequentialImpulseConstraintSolver * constraintSolver;

            std::vector<simulator::Part *> * objectsVec;

            double gravity;

            double simulationTime;

        public:
            BulletEnvironment(std::vector<simulator::Part *> * objects_vec);

            btDiscreteDynamicsWorld * getDynamicsWorld() const;

            void stepSimulation(const double time_step);

            ~BulletEnvironment();
    };

}

#endif // BULLET_ENVIRONMENT_H
