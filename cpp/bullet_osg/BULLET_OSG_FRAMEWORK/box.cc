/* 
 * Bullet OSG Framework.
 * The box module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "box.h"
#include "tools.h"

#include <osg/Geode>
#include <osg/Group>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

simulator::Box::Box(Eigen::Vector3d initial_dimension,
                    Eigen::Vector3d initial_position,
                    Eigen::Vector4d initial_angle,
                    Eigen::Vector3d initial_velocity,
                    Eigen::Vector3d initial_angular_velocity,
                    Eigen::Vector3d initial_inertia,
                    double mass) {

    this->initialDimension = initial_dimension;
    this->initialPosition = initial_position;
    this->initialAngle = initial_angle;
    this->initialInertia = initial_inertia;
    this->initialVelocity = initial_velocity;
    this->initialAngularVelocity = initial_angular_velocity;
    this->mass = mass; 

    // BULLET
    
    /*
     * By default, Bullet considers the following units:
     * - distances are in meters
     * - masses are in kg
     * - time is in seconds
     * - gravity is in meters per square second (9.8 m/s^2)
     *
     * See http://www.bulletphysics.org/mediawiki-1.5.8/index.php?title=Scaling_The_World
     */
    btVector3 bt_box_shape = simulator::vec3_eigen_to_bullet(this->initialDimension / 2.); // this is half lengths...
    this->boxShape = new btBoxShape(bt_box_shape);

    btScalar bt_mass = this->mass;
    btVector3 bt_box_inertia = simulator::vec3_eigen_to_bullet(this->initialInertia);
    this->boxShape->calculateLocalInertia(bt_mass, bt_box_inertia);

    btQuaternion bt_angle = simulator::vec4_eigen_to_bullet(this->initialAngle);
    btVector3 bt_position = simulator::vec3_eigen_to_bullet(this->initialPosition);
    this->boxMotionState = new btDefaultMotionState(btTransform(bt_angle, bt_position));

    btRigidBody::btRigidBodyConstructionInfo box_rigid_body_ci(mass, this->boxMotionState, this->boxShape, bt_box_inertia);
    this->rigidBody = new btRigidBody(box_rigid_body_ci);

    btVector3 bt_velocity = simulator::vec3_eigen_to_bullet(this->initialVelocity);
    this->rigidBody->setLinearVelocity(bt_velocity);

    btVector3 bt_angular_velocity = simulator::vec3_eigen_to_bullet(this->initialAngularVelocity);
    this->rigidBody->setAngularVelocity(bt_angular_velocity);

    // OSG
    this->osgBox = new osg::Box(osg::Vec3(0, 0, 0), this->initialDimension(0), this->initialDimension(1), this->initialDimension(2));
    this->osgShapeDrawable = new osg::ShapeDrawable(this->osgBox);
    this->osgGeode = new osg::Geode();
    this->osgGeode->addDrawable(osgShapeDrawable);

    this->osgGroup = new osg::Group();
    this->osgGroup->addChild(this->osgGeode);
    
    this->osgPAT = new osg::PositionAttitudeTransform();
    this->osgPAT->addChild(this->osgGroup);
}

simulator::Box::~Box() {
    delete this->rigidBody->getMotionState(); // TODO ?
    delete this->rigidBody; // TODO ?

    delete this->boxShape;
    delete this->boxMotionState;

    //delete this->osgBox;
    //delete this->osgShapeDrawable;
    //delete this->osgGeode;
    //delete this->osgPAT;
}

