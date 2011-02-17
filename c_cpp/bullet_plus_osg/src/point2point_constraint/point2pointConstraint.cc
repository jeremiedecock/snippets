#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>

int main(int, char **) {

	// Init OSG /////////////////////////////////////////////////////////////////////////

	// Make the scene graph
	osg::Sphere * sphere = new osg::Sphere(osg::Vec3(0, 0, 0), 2.0f);
	osg::Box * ground = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
	ground->setHalfLengths(osg::Vec3(50, 50, 1));

	osg::ShapeDrawable * sphereSd = new osg::ShapeDrawable(sphere);
	osg::ShapeDrawable * groundSd = new osg::ShapeDrawable(ground);

	osg::Geode * sphereGeode = new osg::Geode();
	osg::Geode * groundGeode = new osg::Geode();
	sphereGeode->addDrawable(sphereSd);
	groundGeode->addDrawable(groundSd);

	osg::PositionAttitudeTransform * spherePat1 = new osg::PositionAttitudeTransform();
	spherePat1->addChild(sphereGeode);
	osg::PositionAttitudeTransform * spherePat2 = new osg::PositionAttitudeTransform();
	spherePat2->addChild(sphereGeode);
	osg::PositionAttitudeTransform * spherePat3 = new osg::PositionAttitudeTransform();
	spherePat3->addChild(sphereGeode);

	osg::Group * root = new osg::Group();
	root->addChild(groundGeode);
	root->addChild(spherePat1);
	root->addChild(spherePat2);
	root->addChild(spherePat3);

	// Setup PATs
	spherePat1->setPosition(osg::Vec3(10, 0, 50));
	spherePat2->setPosition(osg::Vec3(20, 0, 50));
	spherePat3->setPosition(osg::Vec3(30, 0, 50));

	// Make the viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	//viewer.run();
	viewer.getCamera()->setProjectionMatrixAsPerspective(40., 1., 1., 100.);
	osg::Matrix trans;
	trans.makeTranslate(0., 0., 0.);
	osg::Matrix rot;
	rot.makeRotate(3.14, osg::Vec3(1., 0., 0.));
	viewer.getCamera()->setViewMatrix(trans * rot);

	// Init Bullet //////////////////////////////////////////////////////////////////////
	btDbvtBroadphase * broadphase = new btDbvtBroadphase();

	btDefaultCollisionConfiguration * collisionConfiguration = new btDefaultCollisionConfiguration();
	btCollisionDispatcher * dispatcher = new btCollisionDispatcher(collisionConfiguration);

	btSequentialImpulseConstraintSolver * solver = new btSequentialImpulseConstraintSolver();

	btDiscreteDynamicsWorld * dynamicsWorld = new btDiscreteDynamicsWorld(dispatcher,
	                                                                      broadphase,
	                                                                      solver,
	                                                                      collisionConfiguration);
	dynamicsWorld->setGravity(btVector3(0, 0, -10));

	btCollisionShape * fallShape = new btSphereShape(2);

	// Spheres
	btScalar mass = 1;
	btVector3 fallInertia(0, 0, 0);
	fallShape->calculateLocalInertia(mass, fallInertia);

	btDefaultMotionState * fallMotionState1 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                               btVector3(10,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI1(mass,
	                                                          fallMotionState1,
	                                                          fallShape,
	                                                          fallInertia);
	btRigidBody * fallRigidBody1 = new btRigidBody(fallRigidBodyCI1);

	btDefaultMotionState * fallMotionState2 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                               btVector3(20,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI2(mass,
	                                                          fallMotionState2,
	                                                          fallShape,
	                                                          fallInertia);
	btRigidBody * fallRigidBody2 = new btRigidBody(fallRigidBodyCI2);

	btDefaultMotionState * fallMotionState3 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                   btVector3(30,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI3(mass,
	                                                          fallMotionState3,
	                                                          fallShape,
	                                                          fallInertia);
	btRigidBody * fallRigidBody3 = new btRigidBody(fallRigidBodyCI3);

	dynamicsWorld->addRigidBody(fallRigidBody1);
	dynamicsWorld->addRigidBody(fallRigidBody2);
	dynamicsWorld->addRigidBody(fallRigidBody3);

	// Constraints
	btPoint2PointConstraint* p2p1 = new btPoint2PointConstraint(*fallRigidBody1,
								    btVector3(-5, 0, 0));

	btPoint2PointConstraint* p2p2 = new btPoint2PointConstraint(*fallRigidBody1,
	                                                            *fallRigidBody2,
								    btVector3(5, 0, 0),
								    btVector3(-5, 0, 0));

	btPoint2PointConstraint* p2p3 = new btPoint2PointConstraint(*fallRigidBody2,
	                                                            *fallRigidBody3,
								    btVector3(5, 0, 0),
								    btVector3(-5, 0, 0));

	dynamicsWorld->addConstraint(p2p1);
	dynamicsWorld->addConstraint(p2p2);
	dynamicsWorld->addConstraint(p2p3);

	// Main loop ////////////////////////////////////////////////////////////////////////
	while( !viewer.done() ) {

		// Bullet
		dynamicsWorld->stepSimulation(1/60.f,10);
		btTransform trans1, trans2, trans3;
		fallRigidBody1->getMotionState()->getWorldTransform(trans1);
		fallRigidBody2->getMotionState()->getWorldTransform(trans2);
		fallRigidBody3->getMotionState()->getWorldTransform(trans3);

		spherePat1->setPosition(osg::Vec3(trans1.getOrigin().getX(),
		                                  trans1.getOrigin().getY(),
		                                  trans1.getOrigin().getZ()));
		spherePat2->setPosition(osg::Vec3(trans2.getOrigin().getX(),
		                                  trans2.getOrigin().getY(),
		                                  trans2.getOrigin().getZ()));
		spherePat3->setPosition(osg::Vec3(trans3.getOrigin().getX(),
		                                  trans3.getOrigin().getY(),
		                                  trans3.getOrigin().getZ()));

		viewer.frame();
	}

	// Clean Bullet /////////////////////////////////////////////////////////////////////
	dynamicsWorld->removeRigidBody(fallRigidBody1);
	dynamicsWorld->removeRigidBody(fallRigidBody2);
	dynamicsWorld->removeRigidBody(fallRigidBody3);
	delete fallRigidBody1->getMotionState();
	delete fallRigidBody2->getMotionState();
	delete fallRigidBody3->getMotionState();
	delete fallRigidBody1;
	delete fallRigidBody2;
	delete fallRigidBody3;
	delete fallShape;
	delete dynamicsWorld;
	delete solver;
	delete collisionConfiguration;
	delete dispatcher;
	delete broadphase;

	return 0;
}
