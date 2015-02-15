/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include <vector>
#include <iostream>

#include <osg/Geode>
#include <osg/Group>
#include <osg/Material>
#include <osg/PositionAttitudeTransform>
#include <osg/ShapeDrawable>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

// TODO:
// x Utiliser eigen pour les vecteur donnés aux constructeurs des Objets
// x MSAA
// x Black background
// x Light (directional ?)
// x Ajouter et utiliser asseseurs dans Objects
// x Ajouter des fonctions wrapper vec3_eigen_to_bullet, ...
// x Renommer Objects -> Parts
// - Permettre de configurer le refresh rate ou de passer en mode "temps réel" (-1)
// - Scale units factor (mm ?, kg ?, ...)
// - Améliorer l'objet "Ground" (tuiles blanches et noires) + fog + LOD
// - Ombres
// - Key reset
// - Key take screenshot
// - Key start/stop recording -> screencast
// - Faire des vidéos et les poster sur jdhp
// - Séparer les modules
// - Ajouter des objets: sphere, cylindre, etc.
// - Objets STL
//
// - Logs (JSON ?)
// - Permettre de lancer une simulation sans interface graphique (sans osg) -> permetter de remplacer le "physicsCallback"
// - Remplacer le makefile par un cmakelist
// - Créer une arborescence et des modules .h/.cpp
//
// - Vérifier à la main une simulation simple (calculer à la main l'équation d'un objet qui tombe et comparer avec bullet)
//
// - Singleton OSG / Bullet ? -> bof...
// - Caméra
// - Hinges
// - Commandes d'entrée pour hinge
// - Txt infos (hinge constraints, ...)

// OBJECT.CPP /////////////////////////////////////////////////////////////////

#include <btBulletDynamicsCommon.h>

namespace simulator {

    btVector3 vec3_eigen_to_bullet(Eigen::Vector3d eigen_vector) {
        btVector3 bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2));
        return bt_vector;
    }

    btQuaternion vec4_eigen_to_bullet(Eigen::Vector4d eigen_vector) {
        btQuaternion bt_vector(eigen_vector(0), eigen_vector(1), eigen_vector(2), eigen_vector(3));
        return bt_vector;
    }

    class Part {
        protected:
            // Bullet
            btRigidBody * rigidBody;

            // OSG
            osg::Group * osgGroup;
            osg::PositionAttitudeTransform * osgPAT;

        public:
            btRigidBody * getRigidBody() {
                return this->rigidBody;
            }

            osg::Node * getOSGGroup() {
                return this->osgGroup;
            }

            Eigen::Vector3d getPosition() {
                btTransform bulletTransform;
                this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

                Eigen::Vector3d position(bulletTransform.getOrigin().getX(),
                                         bulletTransform.getOrigin().getY(),
                                         bulletTransform.getOrigin().getZ());
                return position;
            }

            Eigen::Vector4d getAngle() {
                btTransform bulletTransform;
                this->rigidBody->getMotionState()->getWorldTransform(bulletTransform);

                Eigen::Vector4d angle(bulletTransform.getRotation().x(),
                                      bulletTransform.getRotation().y(),
                                      bulletTransform.getRotation().z(),
                                      bulletTransform.getRotation().w());
                return angle;
            }

            osg::PositionAttitudeTransform * getOSGPAT() {
                return this->osgPAT;
            }
    };


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
            Box(Eigen::Vector3d initial_dimension, Eigen::Vector3d initial_position, Eigen::Vector4d initial_angle, Eigen::Vector3d initial_velocity, Eigen::Vector3d initial_angular_velocity, Eigen::Vector3d initial_inertia, double mass) {

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

            ~Box() {
                delete this->rigidBody->getMotionState(); // TODO ?
                delete this->rigidBody; // TODO ?

                delete this->boxShape;
                delete this->boxMotionState;

                //delete this->osgBox;
                //delete this->osgShapeDrawable;
                //delete this->osgGeode;
                //delete this->osgPAT;
            }
    };


    class Ground: public simulator::Part {
        private:
            // Bullet
            btCollisionShape * groundShape;
            btDefaultMotionState * groundMotionState;

            // Osg
            osg::Box * osgBox;
            osg::ShapeDrawable * osgShapeDrawable;
            osg::Geode * osgGeode;

        public:
            Ground() {
                // BULLET
                this->groundShape = new btStaticPlaneShape(btVector3(0, 0, 1), 0);

                this->groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1), btVector3(0,0,0)));
                btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0, this->groundMotionState, this->groundShape, btVector3(0, 0, 0));
                this->rigidBody = new btRigidBody(groundRigidBodyCI);

                // OSG
                this->osgBox = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
                this->osgBox->setHalfLengths(osg::Vec3(20, 20, 1));
                this->osgShapeDrawable = new osg::ShapeDrawable(this->osgBox);
                this->osgGeode = new osg::Geode();
                this->osgGeode->addDrawable(osgShapeDrawable);

                this->osgGroup = new osg::Group();
                this->osgGroup->addChild(this->osgGeode);
                
                this->osgPAT = new osg::PositionAttitudeTransform();
                this->osgPAT->addChild(this->osgGroup);
            }

            ~Ground() {
                delete this->rigidBody->getMotionState(); // TODO ?
                delete this->rigidBody; // TODO ?

                delete this->groundShape;
                delete this->groundMotionState;

                //delete this->osgBox;
                //delete this->osgShapeDrawable;
                //delete this->osgGeode;
                //delete this->osgPAT;
            }
    };
}

// BULLET.CPP /////////////////////////////////////////////////////////////////


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

    public:
        BulletEnvironment(std::vector<simulator::Part *> * objects_vec) {
            this->gravity = -10.;

            this->broadphase = new btDbvtBroadphase();

            this->collisionConfiguration = new btDefaultCollisionConfiguration();
            this->collisionDispatcher = new btCollisionDispatcher(this->collisionConfiguration);

            this->constraintSolver = new btSequentialImpulseConstraintSolver();

            this->dynamicsWorld = new btDiscreteDynamicsWorld(this->collisionDispatcher,
                    this->broadphase,
                    this->constraintSolver,
                    this->collisionConfiguration);
            this->dynamicsWorld->setGravity(btVector3(0, 0, this->gravity));

            this->objectsVec = objects_vec;

            // Add rigid bodies
            std::vector<simulator::Part *>::iterator it;
            for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
                this->dynamicsWorld->addRigidBody((*it)->getRigidBody());
            }
        }


        btDiscreteDynamicsWorld * getDynamicsWorld() {
            return this->dynamicsWorld;
        }


        ~BulletEnvironment() {
            std::vector<simulator::Part *>::iterator it;
            for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
                delete (*it);
            }

            delete this->dynamicsWorld;

            delete this->constraintSolver;
            delete this->collisionConfiguration;
            delete this->collisionDispatcher;
            delete this->broadphase;
        }
};


// OSG.CPP ////////////////////////////////////////////////////////////////////


class PhysicsCallback : public osg::NodeCallback {
    // This callback should be applied only to the root osgNode as physics
    // should be updated once per traversal.
    private:
        BulletEnvironment * bulletEnvironment;
        std::vector<simulator::Part *> * objectsVec; //

    public:
        PhysicsCallback(BulletEnvironment * bullet_environment, std::vector<simulator::Part *> * objects_vec) {
            this->bulletEnvironment = bullet_environment;
            this->objectsVec = objects_vec;
        }

        virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
            // Update the physics
            this->bulletEnvironment->getDynamicsWorld()->stepSimulation(1 / 60.f, 10);

            // Update the position of each objects
            std::vector<simulator::Part *>::iterator it;
            for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
                // Bullet
                btTransform bulletTransform;
                (*it)->getRigidBody()->getMotionState()->getWorldTransform(bulletTransform);

                // OSG
                (*it)->getOSGPAT()->setPosition(osg::Vec3(bulletTransform.getOrigin().getX(),
                                                          bulletTransform.getOrigin().getY(),
                                                          bulletTransform.getOrigin().getZ()));
                (*it)->getOSGPAT()->setAttitude(osg::Quat(bulletTransform.getRotation().x(),
                                                          bulletTransform.getRotation().y(),
                                                          bulletTransform.getRotation().z(),
                                                          bulletTransform.getRotation().w()));

                // Debug
                //std::cout << (*it)->getPosition() << std::endl;
                //std::cout << (*it)->getAngle() << std::endl;
            }

            // Continue the traversal
            traverse(node, nv);
        }
};


class OSGEnvironment {

    // TODO: cette classe devrait être un singleton ?!

    private:
        osgViewer::Viewer * viewer;

    public:
        OSGEnvironment(BulletEnvironment * bullet_environment, std::vector<simulator::Part *> * objects_vec) {

            // Make the scene graph
            osg::Group * root = new osg::Group();
            root->setUpdateCallback(new PhysicsCallback(bullet_environment, objects_vec)); // Physics is updated when root is traversed

            // Add objects
            std::vector<simulator::Part *>::iterator it;
            for(it = objects_vec->begin() ; it != objects_vec->end() ; it++) {
                root->addChild((*it)->getOSGPAT());
            }

            // LIGHT ////////////////

            osg::ref_ptr<osg::Light> light = new osg::Light;

            // OSG (as OpenGL) can handle up to 8 light sources.
            // Each light must have a unique number
            //
            // Light number 0 is the default one (integrated to the camera).
            //
            // We do not use light number 0, because we do not want to override the OSG
            // default headlights.
            light->setLightNum(1);

            light->setAmbient(osg::Vec4(1.0, 1.0, 1.0, 0.0));
            light->setDiffuse(osg::Vec4(1.0, 1.0, 1.0, 0.0));
            light->setSpecular(osg::Vec4(1.0, 1.0, 1.0, 1.0));

            // The light's position
            light->setPosition(osg::Vec4(10.0, -10.0, 20.0, 1.0)); // last param w = 0.0 directional light (direction)
                                                                   // w = 1.0 point light (position)
            // Light source
            osg::ref_ptr<osg::LightSource> light_source = new osg::LightSource;    
            light_source->setLight(light);
            root->addChild(light_source);

            osg::ref_ptr<osg::StateSet> state = root->getOrCreateStateSet();
            state->setMode(GL_LIGHT0, osg::StateAttribute::OFF); // GL_LIGHT0 is the default light
            state->setMode(GL_LIGHT1, osg::StateAttribute::ON);  // use GL_LIGHTN for light number N

            // Material
            osg::ref_ptr<osg::Material> mat = new osg::Material;
            mat->setDiffuse(osg::Material::FRONT, osg::Vec4(1.0f, 1.0f, 1.0f, 1.f)); // the diffuse color of the material
            mat->setSpecular(osg::Material::FRONT, osg::Vec4(1.f, 1.f, 1.f, 0.f)); // the specular color of the material
            mat->setShininess(osg::Material::FRONT, 96.f);
            state->setAttribute(mat.get());

            // MAKE THE VIEWER ////////
            this->viewer = new osgViewer::Viewer();
            this->viewer->setSceneData(root);

            // Set the background color (black here -> (0,0,0,0))
            this->viewer->getCamera()->setClearColor(osg::Vec4(0.0f, 0.0f, 0.0f, 0.0f));

            // MSAA: multi-sampled_anti-aliasing 
            // See http://gaming.stackexchange.com/questions/31801/what-are-the-differences-between-the-different-anti-aliasing-multisampling-set
            //     http://osghelp.com/?p=179
            osg::DisplaySettings::instance()->setNumMultiSamples(4); // MSAA: multi-sampled_anti-aliasing 
        }
        
        void run() {
            this->viewer->run();
        }

        ~OSGEnvironment() {
            delete this->viewer;
        }
};


// MAIN.CPP ///////////////////////////////////////////////////////////////////


int main(int, char **) {

    // Init Bullet //////////////////////////////////////////////////////////////////////

    std::vector<simulator::Part *> * objects_vec = new std::vector<simulator::Part *>;
    objects_vec->push_back(new simulator::Ground());
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));

    BulletEnvironment * bullet_environment = new BulletEnvironment(objects_vec);

    // Init OSG /////////////////////////////////////////////////////////////////////////

    OSGEnvironment * osg_environment = new OSGEnvironment(bullet_environment, objects_vec);

    // Run the simulation ///////////////////////////////////////////////////////////////
    
    osg_environment->run();

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    delete bullet_environment;
    delete osg_environment;
    // TODO: delete object_vec and its contents

    return 0;
}
