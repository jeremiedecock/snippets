/* 
 * Bullet Hello
 */

#include <iostream>
#include <btBulletDynamicsCommon.h>

int main (int, char **)
{
	// Init broadphase
	btVector3 worldAabbMin(-10000, -10000, -10000);
	btVector3 worldAabbMax(10000, 10000, 10000);
	int maxProxies = 1024;
	btAxisSweep3* broadphase = new btAxisSweep3(worldAabbMin, worldAabbMax, maxProxies);

	// Init collision configuration
	btDefaultCollisionConfiguration* collisionConfiguration = new btDefaultCollisionConfiguration();
	btCollisionDispatcher* collisionDispatcher = new btCollisionDispatcher(collisionConfiguration);

	// Init constraint solver
	btSequentialImpulseConstraintSolver* constraintSolver = new btSequentialImpulseConstraintSolver();

	// Init world
	btDiscreteDynamicsWorld* dynamicsWorld = new btDiscreteDynamicsWorld(collisionDispatcher,
                                                                             broadphase,
                                                                             constraintSolver,
                                                                             collisionConfiguration);
	dynamicsWorld->setGravity(btVector3(0, -10, 0));

	// Create shapes
	btCollisionShape* groundShape = new btStaticPlaneShape(btVector3(0, 1, 0), 1);
	btCollisionShape* fallShape = new btSphereShape(1);

	// Create Bodies
	btDefaultMotionState* groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),btVector3(0,-1,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,groundMotionState,groundShape,btVector3(0,0,0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);
	dynamicsWorld->addRigidBody(groundRigidBody);

	btDefaultMotionState* fallMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),btVector3(0,50,0)));
	btScalar mass = 1;
	btVector3 fallInertia(0,0,0);
	fallShape->calculateLocalInertia(mass,fallInertia);
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI(mass,fallMotionState,fallShape,fallInertia);
	btRigidBody* fallRigidBody = new btRigidBody(fallRigidBodyCI);
	dynamicsWorld->addRigidBody(fallRigidBody);

	// Main loop
	for (int i=0 ; i<300 ; i++) {
		dynamicsWorld->stepSimulation(1/60.f,10);

		btTransform trans;
		fallRigidBody->getMotionState()->getWorldTransform(trans);

		std::cout << i << " " << trans.getOrigin().getY() << std::endl;
	}

	// Delete objects
	dynamicsWorld->removeRigidBody(fallRigidBody);
	delete fallRigidBody->getMotionState();
	delete fallRigidBody;

	dynamicsWorld->removeRigidBody(groundRigidBody);
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
