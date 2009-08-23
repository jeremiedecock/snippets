#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgProducer/Viewer>

#include <btBulletDynamicsCommon.h>

main() {

	// Init OSG /////////////////////////////////////////////////////////////////////////

	// Make the scene graph
	osg::Capsule *capsule = new osg::Capsule(osg::Vec3(0, 0, 0), 2, 5);
	osg::Box *ground = new osg::Box(osg::Vec3(0, 0, -0.5), 1.0f);
	ground->setHalfLengths(osg::Vec3(50, 50, 0.5));

	osg::ShapeDrawable *capsuleSd = new osg::ShapeDrawable(capsule);
	osg::ShapeDrawable *groundSd = new osg::ShapeDrawable(ground);

	osg::Geode *capsuleGeode = new osg::Geode();
	osg::Geode *groundGeode = new osg::Geode();
	capsuleGeode->addDrawable(capsuleSd);
	groundGeode->addDrawable(groundSd);

	osg::Group *root = new osg::Group();
	root->addChild(groundGeode);

	// Setup PATs
	osg::PositionAttitudeTransform *capsulePATs[3][3][3];
	for(int x=0 ; x<3 ; x++) {
		for(int y=0 ; y<3 ; y++) {
			for(int z=0 ; z<3 ; z++) {
				capsulePATs[x][y][z] = new osg::PositionAttitudeTransform();
				capsulePATs[x][y][z]->addChild(capsuleGeode);
				root->addChild(capsulePATs[x][y][z]);

				capsulePATs[x][y][z]->setPosition(osg::Vec3(x*10, y*10, z*10 + 50)); // Sert juste à règler correctement le recul de la camera du viewer
				// La rotation initiale n'a pas besoin d'être explicité ici car le Geode se
				// calera automatiquement sur le btRigidBody des la première itération
			}
		}
	}

	// Make the viewer
	osgProducer::Viewer viewer;
	viewer.setUpViewer(osgProducer::Viewer::STANDARD_SETTINGS);
	viewer.setSceneData(root);
	viewer.realize();

	// Init Bullet //////////////////////////////////////////////////////////////////////
	//btVector3 worldAabbMin(-10000,-10000,-10000);
	//btVector3 worldAabbMax(10000,10000,10000);
	//int maxProxies = 1024;
	//btAxisSweep3* broadphase = new btAxisSweep3(worldAabbMin,worldAabbMax,maxProxies);
	btDbvtBroadphase* broadphase = new btDbvtBroadphase();

	btDefaultCollisionConfiguration* collisionConfiguration = new btDefaultCollisionConfiguration();
	btCollisionDispatcher* dispatcher = new btCollisionDispatcher(collisionConfiguration);

	btSequentialImpulseConstraintSolver* solver = new btSequentialImpulseConstraintSolver;

	btDiscreteDynamicsWorld* dynamicsWorld = new btDiscreteDynamicsWorld(dispatcher,broadphase,solver,collisionConfiguration);
	dynamicsWorld->setGravity(btVector3(0,-10,0));

	// Shapes
	btCollisionShape* groundShape = new btStaticPlaneShape(btVector3(0,1,0),0);
	//btCollisionShape* fallShape = new btCapsuleShape(0.2, 0.5); // L'effet tunel est probablement du à la trop petite taille des capsules : en fait non... c'est peut être du au timestamp alors
	btCollisionShape* fallShape = new btCapsuleShape(2, 5);

	// Ground
	btDefaultMotionState* groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),btVector3(0,0,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,groundMotionState,groundShape,btVector3(0,0,0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);
	dynamicsWorld->addRigidBody(groundRigidBody);

	// Capsules
	btScalar mass = 1;
	btVector3 fallInertia(0,0,0);
	fallShape->calculateLocalInertia(mass,fallInertia);

	btRigidBody* fallRigidBodies[3][3][3];
	for(int x=0 ; x<3 ; x++) {
		for(int y=0 ; y<3 ; y++) {
			for(int z=0 ; z<3 ; z++) {
				btDefaultMotionState* fallMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
													     btVector3(x*10, y*10 + 50, z*10)));
				btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI(mass,fallMotionState,fallShape,fallInertia);
				fallRigidBodies[x][y][z] = new btRigidBody(fallRigidBodyCI);
				dynamicsWorld->addRigidBody(fallRigidBodies[x][y][z]);
			}
		}
	}

	// Main loop ////////////////////////////////////////////////////////////////////////
	while( !viewer.done() ) {
		viewer.sync();
		viewer.update();

		// Bullet
		dynamicsWorld->stepSimulation(1/60.f,10);

		for(int x=0 ; x<3 ; x++) {
			for(int y=0 ; y<3 ; y++) {
				for(int z=0 ; z<3 ; z++) {
					btTransform trans;
					fallRigidBodies[x][y][z]->getMotionState()->getWorldTransform(trans);

					capsulePATs[x][y][z]->setPosition(osg::Vec3(trans.getOrigin().getX(),trans.getOrigin().getZ(),trans.getOrigin().getY()));
					capsulePATs[x][y][z]->setAttitude(osg::Quat(trans.getRotation().x(),
								       trans.getRotation().z(),
								       trans.getRotation().y(),
								       trans.getRotation().w()));
				}
			}
		}

		viewer.frame();
	}

	// Clean Bullet /////////////////////////////////////////////////////////////////////
	for(int x=0 ; x<3 ; x++) {
		for(int y=0 ; y<3 ; y++) {
			for(int z=0 ; z<3 ; z++) {
				dynamicsWorld->removeRigidBody(fallRigidBodies[x][y][z]);
				delete fallRigidBodies[x][y][z]->getMotionState();
				delete fallRigidBodies[x][y][z];
			}
		}
	}
	dynamicsWorld->removeRigidBody(groundRigidBody);
	delete groundRigidBody->getMotionState();
	delete groundRigidBody;
	delete fallShape;
	delete groundShape;
	delete dynamicsWorld;
	delete solver;
	delete collisionConfiguration;
	delete dispatcher;
	delete broadphase;

	return 0;
}
