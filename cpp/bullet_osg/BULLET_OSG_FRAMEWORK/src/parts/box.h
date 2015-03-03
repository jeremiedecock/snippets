/* 
 * Bullet OSG Framework.
 * The box module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOX_H
#define BOX_H

#include "part.h"

#include <osg/Geode>
#include <osg/Group>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Box: public simulator::Part {
        protected:
            // Bullet
            btCollisionShape * boxShape; // TODO: rename this
            btDefaultMotionState * boxMotionState; // TODO: rename this

            // Osg
            osg::Box * osgBox;
            osg::ShapeDrawable * osgShapeDrawable;
            osg::Geode * osgGeode;

            // Common
            Eigen::Vector3d initialDimension;         // which unit ? mm ?
            Eigen::Vector3d initialPosition;          // which unit ? mm ?
            Eigen::Vector4d initialAngle;             // which unit ? rad ? deg ?
            Eigen::Vector3d initialInertia;           // which unit ? mm/s ?
            Eigen::Vector3d initialVelocity;          // which unit ? mm/s ?
            Eigen::Vector3d initialAngularVelocity;   // which unit ? mm/s ?
            double mass;                              // which unit ? Kg ?

        public:
            Box(Eigen::Vector3d initial_dimension,
                Eigen::Vector3d initial_position,
                Eigen::Vector4d initial_angle,
                Eigen::Vector3d initial_velocity,
                Eigen::Vector3d initial_angular_velocity,
                Eigen::Vector3d initial_inertia,
                double mass);

            ~Box();
    };

}

#endif // BOX_H
