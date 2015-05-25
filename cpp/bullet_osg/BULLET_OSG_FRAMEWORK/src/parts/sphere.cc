/* 
 * Bullet OSG Framework.
 * The sphere module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "sphere.h"
#include "osg_environment.h"
#include "tools/tools.h"

#include <iostream>

#include <osg/Geode>
#include <osg/Group>
#include <osg/Material>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>

#include <Eigen/Dense>

#include <btBulletDynamicsCommon.h>

int botsim::Sphere::numInstances = 0;

botsim::Sphere::Sphere(double initial_radius,
                          Eigen::Vector3d initial_position,
                          Eigen::Vector4d initial_angle,
                          Eigen::Vector3d initial_velocity,
                          Eigen::Vector3d initial_angular_velocity,
                          Eigen::Vector3d initial_inertia,
                          double mass,
                          double friction,
                          double rolling_friction,
                          double restitution,
                          std::string name) {

    this->initialRadius = initial_radius;
    this->initialPosition = initial_position;
    this->initialAngle = initial_angle;
    this->initialInertia = initial_inertia;
    this->initialVelocity = initial_velocity;
    this->initialAngularVelocity = initial_angular_velocity;
    this->mass = mass; 
    this->friction = friction; 
    this->rollingFriction = rolling_friction; 
    this->restitution = restitution; 

    // Define the name of this instance
    if(name != "") {
        this->name = name;
    } else {
        // Default name
        Sphere::numInstances++;
        this->name = "sphere" + std::to_string(Sphere::numInstances); // C++11 only ; see http://stackoverflow.com/questions/191757/c-concatenate-string-and-int
    }

    //std::cout << "build " << this->name << std::endl;

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
    this->sphereShape = new btSphereShape(this->initialRadius);

    btScalar bt_mass = this->mass;
    btVector3 bt_sphere_inertia = botsim::vec3_eigen_to_bullet(this->initialInertia);
    this->sphereShape->calculateLocalInertia(bt_mass, bt_sphere_inertia);

    btQuaternion bt_angle = botsim::vec4_eigen_to_bullet(this->initialAngle);
    btVector3 bt_position = botsim::vec3_eigen_to_bullet(this->initialPosition);
    this->sphereMotionState = new btDefaultMotionState(btTransform(bt_angle, bt_position));

    btRigidBody::btRigidBodyConstructionInfo sphere_rigid_body_ci(mass, this->sphereMotionState, this->sphereShape, bt_sphere_inertia);
    /* 
     * Restitution and friction
     * see: http://stackoverflow.com/questions/8289653/bouncing-ball-in-bullet
     *      http://bulletphysics.org/Bullet/phpBB3/viewtopic.php?t=6783
     *      http://bulletphysics.org/Bullet/BulletFull/structbtRigidBody_1_1btRigidBodyConstructionInfo.html
     */
    //sphere_rigid_body_ci.m_linearDamping = 0.;
    //sphere_rigid_body_ci.m_angularDamping = 0.;
    sphere_rigid_body_ci.m_friction = this->friction;
    sphere_rigid_body_ci.m_rollingFriction = this->rollingFriction;
    sphere_rigid_body_ci.m_restitution = this->restitution;
    //sphere_rigid_body_ci.m_linearSleepingThreshold = 0.;
    //sphere_rigid_body_ci.m_angularSleepingThreshold = 0.;
    //sphere_rigid_body_ci.m_additionalDamping = false;
    //sphere_rigid_body_ci.m_additionalDampingFactor = 0.;
    //sphere_rigid_body_ci.m_additionalLinearDampingThresholdSqr = 0.;
    //sphere_rigid_body_ci.m_additionalAngularDampingThresholdSqr = 0.;
    //sphere_rigid_body_ci.m_additionalAngularDampingFactor = 0.;
    this->rigidBody = new btRigidBody(sphere_rigid_body_ci);

    btVector3 bt_velocity = botsim::vec3_eigen_to_bullet(this->initialVelocity);
    this->rigidBody->setLinearVelocity(bt_velocity);

    btVector3 bt_angular_velocity = botsim::vec3_eigen_to_bullet(this->initialAngularVelocity);
    this->rigidBody->setAngularVelocity(bt_angular_velocity);

    // OSG
    this->osgSphere = new osg::Sphere(osg::Vec3(0, 0, 0), this->initialRadius);
    this->osgShapeDrawable = new osg::ShapeDrawable(this->osgSphere);
    this->osgGeode = new osg::Geode();
    this->osgGeode->addDrawable(osgShapeDrawable);

    this->osgGroup = new osg::Group();
    this->osgGroup->addChild(this->osgGeode);
    
    // Create and set material
    // See http://www.sm.luth.se/csee/courses/smm/011/l/t2.pdf
    osg::ref_ptr<osg::StateSet> p_state_set = new osg::StateSet();

    osg::ref_ptr<osg::Material> p_material = new osg::Material();

    p_material->setAmbient(osg::Material::FRONT_AND_BACK,  osg::Vec4(1.0f, 1.0f, 1.0f, 1.f));
    p_material->setDiffuse(osg::Material::FRONT_AND_BACK,  osg::Vec4(1.0f, 0.5f, 0.1f, 1.f));  // The "base color" of the object
    p_material->setSpecular(osg::Material::FRONT_AND_BACK, osg::Vec4(1.0f, 0.5f, 0.1f, 1.f));
    p_material->setShininess(osg::Material::FRONT_AND_BACK, 63.f);    // 0. to 128.

    // Associate material with the stateset
    p_state_set->setAttribute(p_material);

    // Associate stateset with the geode
    this->osgGeode->setStateSet(p_state_set);

    // Set the mask for shadows -> this object casts and receives shadows
    this->osgGroup->setNodeMask(botsim::OSGEnvironment::castsShadowTraversalMask | botsim::OSGEnvironment::receivesShadowTraversalMask);
    
    this->osgPAT = new osg::PositionAttitudeTransform();
    this->osgPAT->addChild(this->osgGroup);
}

botsim::Sphere::~Sphere() {
    delete this->rigidBody->getMotionState(); // TODO ?
    delete this->rigidBody; // TODO ?

    delete this->sphereShape;
    delete this->sphereMotionState;

    //delete this->osgSphere;
    //delete this->osgShapeDrawable;
    //delete this->osgGeode;
    //delete this->osgPAT;
}

std::string botsim::Sphere::getName() const {
    return this->name;
}

