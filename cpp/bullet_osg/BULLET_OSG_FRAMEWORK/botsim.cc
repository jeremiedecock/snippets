#include <vector>
#include <iostream>

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

// TODO:
// - Utiliser eigen pour les vecteur donnés aux constructeurs des Objets
// - Permettre de configurer le refresh rate ou de passer en mode "temps réel"
// - Ajouter des objets: sphere, cylindre, etc.
// - Objets STL
// - Améliorer scène OSG (MSAA, background, lumière, ...)
// - Améliorer l'objet "Ground" (tuiles blanches et noires) + fog + LOD
// - Key start/stop recording -> screencast
// - Key take screenshot
// - Key reset
// - Ombres
// - Faire des vidéos et les poster sur jdhp
//
// - Logs (JSON ?)
// - Permettre de lancer une simulation sans interface graphique (sans osg) -> permetter de remplacer le "physicsCallback"
// - Séparer les modules
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
            double width;  // which unit ? mm ?
            double depth;  // which unit ? mm ?
            double height; // which unit ? mm ?
            double mass;   // which unit ? Kg ?

        public:
            // TODO: eigenvect dimensions, eigenvect position, eigenvect initial_inertia, double mass
            Box(double _width, double _depth, double _height, double position_x, double position_y, double position_z, double _mass) : width(_width), depth(_depth), height(_height), mass(_mass) {

                // BULLET
                this->boxShape = new btBoxShape(btVector3(this->width/2., this->depth/2., this->height/2.)); // ce sont des half lengths

                btScalar mass = this->mass;
                btVector3 boxInertia(0, 0, 0);
                this->boxShape->calculateLocalInertia(mass, boxInertia);

                this->boxMotionState = new btDefaultMotionState(btTransform(btQuaternion(1,1,1,25),
                                                                btVector3(position_x, position_y, position_z)));
                btRigidBody::btRigidBodyConstructionInfo boxRigidBodyCI(mass,
                        this->boxMotionState,
                        this->boxShape,
                        boxInertia);
                this->rigidBody = new btRigidBody(boxRigidBodyCI);

                // OSG
                this->osgBox = new osg::Box(osg::Vec3(0, 0, 0), this->width, this->depth, this->height);
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

                this->groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
                            btVector3(0,0,0)));
                btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,
                        this->groundMotionState,
                        this->groundShape,
                        btVector3(0, 0, 0));
                this->rigidBody = new btRigidBody(groundRigidBodyCI);

                // OSG
                this->osgBox = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
                this->osgBox->setHalfLengths(osg::Vec3(15, 15, 1));
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
    objects_vec->push_back(new botsim::Box(1., 1., 1., 0., 0., 20., 1.));
    objects_vec->push_back(new botsim::Box(1., 2., 1., 0., 0., 30., 1.));
    objects_vec->push_back(new botsim::Box(2., 2., 2., 0., 0., 40., 1.));
    objects_vec->push_back(new botsim::Box(3., 1., 1., 0., 0., 50., 5.));

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
