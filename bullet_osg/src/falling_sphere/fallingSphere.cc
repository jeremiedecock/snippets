#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>

btRigidBody *fallRigidBody;
btDiscreteDynamicsWorld *dynamicsWorld;

class BulletCB:public osg::NodeCallback {
	public:
		virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
			osg::PositionAttitudeTransform * pat =
				dynamic_cast < osg::PositionAttitudeTransform * >(node);

			dynamicsWorld->stepSimulation(1 / 60.f, 10);
			btTransform bulletTransform;
			fallRigidBody->getMotionState()->getWorldTransform(bulletTransform);

			pat->setPosition(osg::Vec3(bulletTransform.getOrigin().getX(),
			                           bulletTransform.getOrigin().getY(),
			                           bulletTransform.getOrigin().getZ()));

			traverse(node, nv);
		}
};

int main(int, char **) {

	// Init Bullet //////////////////////////////////////////////////////////////////////

	btDbvtBroadphase * broadphase = new btDbvtBroadphase();

	btDefaultCollisionConfiguration * collisionConfiguration = new btDefaultCollisionConfiguration();
	btCollisionDispatcher * collisionDispatcher = new btCollisionDispatcher(collisionConfiguration);

	btSequentialImpulseConstraintSolver * constraintSolver = new btSequentialImpulseConstraintSolver();

	dynamicsWorld = new btDiscreteDynamicsWorld(collisionDispatcher,
	                                            broadphase,
	                                            constraintSolver,
	                                            collisionConfiguration);
	dynamicsWorld->setGravity(btVector3(0, 0, -10));

	btCollisionShape * groundShape = new btStaticPlaneShape(btVector3(0, 0, 1), 0);
	btCollisionShape * fallShape = new btSphereShape(1);

	// Ground
	btDefaultMotionState * groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                                btVector3(0,0,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,
	                                                           groundMotionState,
	                                                           groundShape,
	                                                           btVector3(0, 0, 0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);

	// Sphere
	btScalar mass = 1;
	btVector3 fallInertia(0, 0, 0);
	fallShape->calculateLocalInertia(mass, fallInertia);

	btDefaultMotionState * fallMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                              btVector3(0,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI(mass,
	                                                         fallMotionState,
	                                                         fallShape,
	                                                         fallInertia);
	fallRigidBody = new btRigidBody(fallRigidBodyCI);

	// Add rigid bodies
	dynamicsWorld->addRigidBody(groundRigidBody);
	dynamicsWorld->addRigidBody(fallRigidBody);

	// Init OSG /////////////////////////////////////////////////////////////////////////

	// Make the scene graph
	osg::Sphere * sphere = new osg::Sphere(osg::Vec3(0, 0, 0), 1.0f);
	osg::Box * ground = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
	ground->setHalfLengths(osg::Vec3(50, 50, 1));

	osg::ShapeDrawable * sphereSd = new osg::ShapeDrawable(sphere);
	osg::ShapeDrawable * groundSd = new osg::ShapeDrawable(ground);

	osg::Geode * sphereGeode = new osg::Geode();
	osg::Geode * groundGeode = new osg::Geode();
	sphereGeode->addDrawable(sphereSd);
	groundGeode->addDrawable(groundSd);

	osg::PositionAttitudeTransform * spherePat = new osg::PositionAttitudeTransform();
	spherePat->setUpdateCallback(new BulletCB);
	spherePat->addChild(sphereGeode);

	osg::Group * root = new osg::Group();
	root->addChild(groundGeode);
	root->addChild(spherePat);

	// Make the viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	// Clean Bullet /////////////////////////////////////////////////////////////////////

	dynamicsWorld->removeRigidBody(fallRigidBody);
	dynamicsWorld->removeRigidBody(groundRigidBody);
	delete fallRigidBody->getMotionState();
	delete fallRigidBody;
	delete groundRigidBody->getMotionState();
	delete groundRigidBody;
	delete fallShape;
	delete groundShape;
	delete dynamicsWorld;
	delete constraintSolver;
	delete collisionConfiguration;
	delete collisionDispatcher;
	delete broadphase;

	return 0;
}
