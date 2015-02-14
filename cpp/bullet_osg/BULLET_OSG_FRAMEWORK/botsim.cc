#include <vector>
#include <iostream>

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <Eigen/Dense>

// TODO:
// x Utiliser eigen pour les vecteur donnés aux constructeurs des Objets
// - MSAA
// - Black background
// - Permettre de configurer le refresh rate ou de passer en mode "temps réel"
// - Séparer les modules
// - Ajouter des objets: sphere, cylindre, etc.
// - Objets STL
// - Light
// - Améliorer l'objet "Ground" (tuiles blanches et noires) + fog + LOD
// - Key start/stop recording -> screencast
// - Key take screenshot
// - Key reset
// - Ombres
// - Faire des vidéos et les poster sur jdhp
//
// - Logs (JSON ?)
// - Permettre de lancer une simulation sans interface graphique (sans osg) -> permetter de remplacer le "physicsCallback"
// - Remplacer le makefile par un cmakelist
// - Créer une arborescence et des modules .h/.cpp
//
// - Check units (mm ?, kg ?, ...)
// - Vérifier à la main une simulation simple (calculer à la main l'équation d'un objet qui tombe et comparer avec bullet)
//
// - Singleton OSG / Bullet ? -> bof...
// - Caméra
// - Hinges
// - Commandes d'entrée pour hinge
// - Txt infos (hinge constraints, ...)

// OBJECT.CPP /////////////////////////////////////////////////////////////////

#include <btBulletDynamicsCommon.h>

namespace botsim {

    class Object {
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

            osg::PositionAttitudeTransform * getOSGPAT() {
                return this->osgPAT;
            }
    };


    class Box: public botsim::Object {
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
                btVector3 bt_box_shape(this->initialDimension(0)/2., this->initialDimension(1)/2., this->initialDimension(2)/2.);
                this->boxShape = new btBoxShape(bt_box_shape); // this is half lengths...

                btScalar bt_mass = this->mass;
                btVector3 bt_box_inertia(this->initialInertia(0), this->initialInertia(1), this->initialInertia(2));
                this->boxShape->calculateLocalInertia(bt_mass, bt_box_inertia);

                btQuaternion bt_angle(this->initialAngle(0), this->initialAngle(1), this->initialAngle(2), this->initialAngle(3));
                btVector3 bt_position(this->initialPosition(0), this->initialPosition(1), this->initialPosition(2));
                this->boxMotionState = new btDefaultMotionState(btTransform(bt_angle, bt_position));

                btRigidBody::btRigidBodyConstructionInfo box_rigid_body_ci(mass, this->boxMotionState, this->boxShape, bt_box_inertia);
                this->rigidBody = new btRigidBody(box_rigid_body_ci);

                btVector3 bt_velocity(this->initialVelocity(0), this->initialVelocity(1), this->initialVelocity(2));
                this->rigidBody->setLinearVelocity(bt_velocity);

                btVector3 bt_angular_velocity(this->initialAngularVelocity(0), this->initialAngularVelocity(1), this->initialAngularVelocity(2));
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


    class Ground: public botsim::Object {
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

        std::vector<botsim::Object *> * objectsVec;

        double gravity;

    public:
        BulletEnvironment(std::vector<botsim::Object *> * objects_vec) {
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
            std::vector<botsim::Object *>::iterator it;
            for(it = this->objectsVec->begin() ; it != this->objectsVec->end() ; it++) {
                this->dynamicsWorld->addRigidBody((*it)->getRigidBody());
            }
        }


        btDiscreteDynamicsWorld * getDynamicsWorld() {
            return this->dynamicsWorld;
        }


        ~BulletEnvironment() {
            std::vector<botsim::Object *>::iterator it;
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
        std::vector<botsim::Object *> * objectsVec; //

    public:
        PhysicsCallback(BulletEnvironment * bullet_environment, std::vector<botsim::Object *> * objects_vec) {
            this->bulletEnvironment = bullet_environment;
            this->objectsVec = objects_vec;
        }

        virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
            // Update the physics
            this->bulletEnvironment->getDynamicsWorld()->stepSimulation(1 / 60.f, 10);

            // Update the position of each objects
            std::vector<botsim::Object *>::iterator it;
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
                //std::cout << bulletTransform.getOrigin().getZ() << std::endl;
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
        OSGEnvironment(BulletEnvironment * bullet_environment, std::vector<botsim::Object *> * objects_vec) {

            // Make the scene graph
            osg::Group * root = new osg::Group();
            root->setUpdateCallback(new PhysicsCallback(bullet_environment, objects_vec)); // Physics is updated when root is traversed

            // Add objects
            std::vector<botsim::Object *>::iterator it;
            for(it = objects_vec->begin() ; it != objects_vec->end() ; it++) {
                root->addChild((*it)->getOSGPAT());
            }

            // Make the viewer
            this->viewer = new osgViewer::Viewer();
            this->viewer->setSceneData(root);
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

    std::vector<botsim::Object *> * objects_vec = new std::vector<botsim::Object *>;
    objects_vec->push_back(new botsim::Ground());
    objects_vec->push_back(new botsim::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new botsim::Box(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new botsim::Box(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.));
    objects_vec->push_back(new botsim::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));

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
