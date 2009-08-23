#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>
#include <iostream>

btDiscreteDynamicsWorld * dynamicsWorld;

btRigidBody * rb1;
btRigidBody * rb2;

btSliderConstraint * sc1;

osg::PositionAttitudeTransform * boxPat1;
osg::PositionAttitudeTransform * boxPat2;

class physicsCallback : public osg::NodeCallback {
	public:
		virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
			static btClock * clock = new btClock();

			dynamicsWorld->stepSimulation(1 / 60.f, 10);

			btTransform bulletTransform1;
			btTransform bulletTransform2;

			rb1->getMotionState()->getWorldTransform(bulletTransform1);
			rb2->getMotionState()->getWorldTransform(bulletTransform2);

			boxPat1->setPosition(osg::Vec3(bulletTransform1.getOrigin().getX(),
			                           bulletTransform1.getOrigin().getY(),
			                           bulletTransform1.getOrigin().getZ()));
			boxPat1->setAttitude(osg::Quat(bulletTransform1.getRotation().x(),
			                           bulletTransform1.getRotation().y(),
			                           bulletTransform1.getRotation().z(),
			                           bulletTransform1.getRotation().w()));

			boxPat2->setPosition(osg::Vec3(bulletTransform2.getOrigin().getX(),
			                           bulletTransform2.getOrigin().getY(),
			                           bulletTransform2.getOrigin().getZ()));
			boxPat2->setAttitude(osg::Quat(bulletTransform2.getRotation().x(),
			                           bulletTransform2.getRotation().y(),
			                           bulletTransform2.getRotation().z(),
			                           bulletTransform2.getRotation().w()));

			double t = clock->getTimeMilliseconds();
			double ft = 5.0 * sin(t / 500.0 + 3.14);
			std::cout << "f(" << t << ") = " << ft << std::endl;
			sc1->setTargetLinMotorVelocity(ft);
	
			traverse(node, nv);
		}
};

int main(int, char **) {

	// Init OSG /////////////////////////////////////////////////////////////////////////

	// Make the scene graph
	osg::Box * box = new osg::Box(osg::Vec3(0, 0, 0), 2.0f);
	osg::Box * ground = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
	ground->setHalfLengths(osg::Vec3(50, 50, 1));

	osg::ShapeDrawable * boxSd = new osg::ShapeDrawable(box);
	osg::ShapeDrawable * groundSd = new osg::ShapeDrawable(ground);

	osg::Geode * boxGeode = new osg::Geode();
	osg::Geode * groundGeode = new osg::Geode();
	boxGeode->addDrawable(boxSd);
	groundGeode->addDrawable(groundSd);

	boxPat1 = new osg::PositionAttitudeTransform();
	boxPat1->addChild(boxGeode);

	boxPat2 = new osg::PositionAttitudeTransform();
	boxPat2->addChild(boxGeode);

	osg::Group * root = new osg::Group();
	root->addChild(groundGeode);
	root->addChild(boxPat1);
	root->addChild(boxPat2);

	// Init Bullet //////////////////////////////////////////////////////////////////////
	btDbvtBroadphase * broadphase = new btDbvtBroadphase();

	btDefaultCollisionConfiguration * collisionConfiguration = new btDefaultCollisionConfiguration();
	btCollisionDispatcher * dispatcher = new btCollisionDispatcher(collisionConfiguration);

	btSequentialImpulseConstraintSolver * solver = new btSequentialImpulseConstraintSolver();

	dynamicsWorld = new btDiscreteDynamicsWorld(dispatcher,
	                                            broadphase,
	                                            solver,
	                                            collisionConfiguration);
	dynamicsWorld->setGravity(btVector3(0, 0, -10));

	btCollisionShape * groundShape = new btStaticPlaneShape(btVector3(0, 0, 1), 0);
	btCollisionShape * boxShape = new btBoxShape(btVector3(1, 1, 1));

	// Ground
	btDefaultMotionState * groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                                btVector3(0,0,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,
	                                                           groundMotionState,
	                                                           groundShape,
	                                                           btVector3(0, 0, 0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);

	dynamicsWorld->addRigidBody(groundRigidBody);

	// Boxes
	btScalar mass = 1;
	btVector3 fallInertia(0, 0, 0);
	boxShape->calculateLocalInertia(mass, fallInertia);

	btDefaultMotionState * fallMotionState1 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                               btVector3(0,0,10)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI1(mass,
	                                                          fallMotionState1,
	                                                          boxShape,
	                                                          fallInertia);
	rb1 = new btRigidBody(fallRigidBodyCI1);


	btDefaultMotionState * fallMotionState2 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                               btVector3(0,0,30)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI2(0,
	                                                          fallMotionState2,
	                                                          boxShape,
	                                                          btVector3(0, 0, 0));
	rb2 = new btRigidBody(fallRigidBodyCI2);


	dynamicsWorld->addRigidBody(rb1);
	dynamicsWorld->addRigidBody(rb2);

	// Constraints
	btTransform transformA, transformB;
	transformA = btTransform::getIdentity();
	transformB = btTransform::getIdentity();

	btTransform rb1t = rb1->getCenterOfMassTransform();
	btVector3 up(rb1t.getBasis()[0][0],
	             rb1t.getBasis()[1][0],
	             rb1t.getBasis()[2][0]);
        btVector3 direction = (rb2->getWorldTransform().getOrigin() - rb1->getWorldTransform().getOrigin()).normalize();

	btScalar angle = acos(up.dot(direction));
        btVector3 axis = up.cross(direction);

        transformA.setRotation(btQuaternion(axis, angle));
        transformB.setRotation(btQuaternion(axis, angle));
		
	sc1 = new btSliderConstraint(*rb1,
	                             *rb2,
	                             transformA,
	                             transformB,
	                             true);

	dynamicsWorld->addConstraint(sc1);
	
	sc1->setMaxLinMotorForce(5);
	sc1->setPoweredLinMotor(true);

	// Make the viewer
	root->setUpdateCallback(new physicsCallback);
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	// Clean Bullet /////////////////////////////////////////////////////////////////////
	dynamicsWorld->removeRigidBody(rb1);
	dynamicsWorld->removeRigidBody(rb2);
	delete rb1->getMotionState();
	delete rb2->getMotionState();
	delete rb1;
	delete rb2;
	delete boxShape;
	delete dynamicsWorld;
	delete solver;
	delete collisionConfiguration;
	delete dispatcher;
	delete broadphase;

	return 0;
}
