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

#include <chrono>
#include <set>

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

            double gravity;

            /**
             * The time within the simulation.
             */
            double simulationTimeSec;

            /**
             * The actual user start time (i.e. outside the simulation).
             */
            std::chrono::time_point<std::chrono::system_clock> userStartTime;

            int bulletMaxSubSteps;

            double bulletFixedTimeSubStepSec;

        public:
            std::set<simulator::Part *> * partsSet;

        public:
            BulletEnvironment(std::set<simulator::Part *> * parts_set);

            ~BulletEnvironment();

            btDiscreteDynamicsWorld * getDynamicsWorld() const;

            void stepSimulation(const double time_step_sec);

            void stepSimulation();

            void resetSimulation();

            /**
             * Return the time within the simulation.
             */
            double getElapsedSimulationTimeSec() const;

            /**
             * Return the actual user time i.e. outside the simulation.
             */
            double getElapsedUserTimeSec() const;
    };

}

#endif // BULLET_ENVIRONMENT_H
