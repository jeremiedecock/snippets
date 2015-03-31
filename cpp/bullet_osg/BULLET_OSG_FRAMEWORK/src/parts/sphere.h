/* 
 * Bullet OSG Framework.
 * The sphere module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef SPHERE_H
#define SPHERE_H

#include "part.h"

#include <osg/Geode>
#include <osg/Group>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Sphere: public simulator::Part {
        protected:
            // Bullet
            btCollisionShape * sphereShape; // TODO: rename this
            btDefaultMotionState * sphereMotionState; // TODO: rename this

            // Osg
            osg::Sphere * osgSphere;
            osg::ShapeDrawable * osgShapeDrawable;
            osg::Geode * osgGeode;

            // Common
            std::string name;                         // the name of this instance
            double initialRadius;                     // which unit ? mm ?
            Eigen::Vector3d initialPosition;          // which unit ? mm ?
            Eigen::Vector4d initialAngle;             // which unit ? rad ? deg ?
            Eigen::Vector3d initialInertia;           // which unit ? mm/s ?
            Eigen::Vector3d initialVelocity;          // which unit ? mm/s ?
            Eigen::Vector3d initialAngularVelocity;   // which unit ? mm/s ?

        protected:
            static int numInstances;

        public:
            Sphere(double initial_radius,
                   Eigen::Vector3d initial_position,
                   Eigen::Vector4d initial_angle,
                   Eigen::Vector3d initial_velocity,
                   Eigen::Vector3d initial_angular_velocity,
                   Eigen::Vector3d initial_inertia,
                   double mass,
                   std::string name="");

            ~Sphere();

            std::string getName() const;
    };

}

#endif // SPHERE_H
