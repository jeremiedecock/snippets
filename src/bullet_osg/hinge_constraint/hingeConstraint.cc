#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>

btDiscreteDynamicsWorld * dynamicsWorld;

btRigidBody * fallRigidBody1;
btRigidBody * fallRigidBody2;
btRigidBody * fallRigidBody3;

osg::PositionAttitudeTransform * spherePat1;
osg::PositionAttitudeTransform * spherePat2;
osg::PositionAttitudeTransform * spherePat3;

class physicsCallback : public osg::NodeCallback {
	public:
		virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
			dynamicsWorld->stepSimulation(1 / 60.f, 10);

			btTransform bulletTransform1;
			btTransform bulletTransform2;
			btTransform bulletTransform3;

			fallRigidBody1->getMotionState()->getWorldTransform(bulletTransform1);
			fallRigidBody2->getMotionState()->getWorldTransform(bulletTransform2);
			fallRigidBody3->getMotionState()->getWorldTransform(bulletTransform3);

			spherePat1->setPosition(osg::Vec3(bulletTransform1.getOrigin().getX(),
			                           bulletTransform1.getOrigin().getY(),
			                           bulletTransform1.getOrigin().getZ()));
			spherePat1->setAttitude(osg::Quat(bulletTransform1.getRotation().x(),
			                           bulletTransform1.getRotation().y(),
			                           bulletTransform1.getRotation().z(),
			                           bulletTransform1.getRotation().w()));
	
			spherePat2->setPosition(osg::Vec3(bulletTransform2.getOrigin().getX(),
			                            bulletTransform2.getOrigin().getY(),
			                            bulletTransform2.getOrigin().getZ()));
			spherePat2->setAttitude(osg::Quat(bulletTransform2.getRotation().x(),
			                            bulletTransform2.getRotation().y(),
			                            bulletTransform2.getRotation().z(),
			                            bulletTransform2.getRotation().w()));
	
			spherePat3->setPosition(osg::Vec3(bulletTransform3.getOrigin().getX(),
			                            bulletTransform3.getOrigin().getY(),
			                            bulletTransform3.getOrigin().getZ()));
			spherePat3->setAttitude(osg::Quat(bulletTransform3.getRotation().x(),
			                            bulletTransform3.getRotation().y(),
			                            bulletTransform3.getRotation().z(),
			                            bulletTransform3.getRotation().w()));

			traverse(node, nv);
		}
};

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

	spherePat1 = new osg::PositionAttitudeTransform();
	spherePat2 = new osg::PositionAttitudeTransform();
	spherePat3 = new osg::PositionAttitudeTransform();
	spherePat1->addChild(sphereGeode);
	spherePat2->addChild(sphereGeode);
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
	fallRigidBody1 = new btRigidBody(fallRigidBodyCI1);

	btDefaultMotionState * fallMotionState2 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                               btVector3(20,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI2(mass,
	                                                          fallMotionState2,
	                                                          fallShape,
	                                                          fallInertia);
	fallRigidBody2 = new btRigidBody(fallRigidBodyCI2);

	btDefaultMotionState * fallMotionState3 = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                   btVector3(30,0,50)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI3(mass,
	                                                          fallMotionState3,
	                                                          fallShape,
	                                                          fallInertia);
	fallRigidBody3 = new btRigidBody(fallRigidBodyCI3);

	dynamicsWorld->addRigidBody(fallRigidBody1);
	dynamicsWorld->addRigidBody(fallRigidBody2);
	dynamicsWorld->addRigidBody(fallRigidBody3);

	// Constraints
	const btVector3 btPivotA( -5.0f, 0.0f, 0.0f );
	const btVector3 btPivotB( 5.0f, 0.0f, 0.0f );
	btVector3 btAxisA( 0.0f, 1.0f, 0.0f );
	btVector3 btAxisB( 0.0f, 1.0f, 0.0f );
	btHingeConstraint* hc1 = new btHingeConstraint(*fallRigidBody1,
					               btPivotA,
						       btAxisA);

	btHingeConstraint* hc2 = new btHingeConstraint(*fallRigidBody1,
	                                               *fallRigidBody2,
					               btPivotB,
					               btPivotA,
						       btAxisA,
						       btAxisB);

	btHingeConstraint* hc3 = new btHingeConstraint(*fallRigidBody2,
	                                               *fallRigidBody3,
					               btPivotB,
					               btPivotA,
						       btAxisA,
						       btAxisB);

	dynamicsWorld->addConstraint(hc1);
	dynamicsWorld->addConstraint(hc2);
	dynamicsWorld->addConstraint(hc3);

	// Make the viewer
	root->setUpdateCallback(new physicsCallback);
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();


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
