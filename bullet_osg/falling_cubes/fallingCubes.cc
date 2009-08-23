#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>

btDiscreteDynamicsWorld * dynamicsWorld;

class bodyDataType : public osg::Referenced {
	public:
		bodyDataType(btCollisionShape * collisionShape, int x, int y, int z) {
			btScalar mass = 1;
			btVector3 inertia(0, 0, 0);
			collisionShape->calculateLocalInertia(mass, inertia);

			btDefaultMotionState * motionState = 
					new btDefaultMotionState(btTransform(btQuaternion(0, 0, 0, 1),
								 btVector3(x, y, z + 20)));
			btRigidBody::btRigidBodyConstructionInfo rigidBodyCI(mass,
										 motionState,
										 collisionShape,
										 inertia);
			rigidBody = new btRigidBody(rigidBodyCI);
			dynamicsWorld->addRigidBody(rigidBody);
		}

		btRigidBody* getRigidBody() {
			return rigidBody;
		}

	private:
		btRigidBody * rigidBody;
};

class physicsCallback : public osg::NodeCallback {
	public:
		virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
			dynamicsWorld->stepSimulation(1 / 60.f, 10);
			traverse(node, nv);
		}
};

class bodyCallback : public osg::NodeCallback {
	public:
		virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
			osg::PositionAttitudeTransform * pat =
				dynamic_cast < osg::PositionAttitudeTransform * >(node);

			bodyDataType * bodyData = dynamic_cast < bodyDataType * >(pat->getUserData());

			btTransform bulletTransform;
			bodyData->getRigidBody()->getMotionState()->getWorldTransform(bulletTransform);

			pat->setPosition(osg::Vec3(bulletTransform.getOrigin().getX(),
			                           bulletTransform.getOrigin().getY(),
			                           bulletTransform.getOrigin().getZ()));
			pat->setAttitude(osg::Quat(bulletTransform.getRotation().x(),
			                           bulletTransform.getRotation().y(),
			                           bulletTransform.getRotation().z(),
			                           bulletTransform.getRotation().w()));

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
	btCollisionShape * fallShape = new btBoxShape(btVector3(0.5, 0.5, 0.5)); // ce sont des half lengths

	// Ground
	btDefaultMotionState * groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                                btVector3(0,0,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,
	                                                           groundMotionState,
	                                                           groundShape,
	                                                           btVector3(0, 0, 0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);
	dynamicsWorld->addRigidBody(groundRigidBody);

	// Init OSG /////////////////////////////////////////////////////////////////////////

	// Make the scene graph
	osg::Box * box = new osg::Box(osg::Vec3(0, 0, 0), 1.0f);
	osg::Box * ground = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
	ground->setHalfLengths(osg::Vec3(15, 15, 1));

	osg::ShapeDrawable * boxSd = new osg::ShapeDrawable(box);
	osg::ShapeDrawable * groundSd = new osg::ShapeDrawable(ground);

	osg::Geode * boxGeode = new osg::Geode();
	osg::Geode * groundGeode = new osg::Geode();
	boxGeode->addDrawable(boxSd);
	groundGeode->addDrawable(groundSd);

	osg::Group *root = new osg::Group();
	root->setUpdateCallback(new physicsCallback);
	root->addChild(groundGeode);

	// Setup Transforms
	bodyCallback * bodyCB = new bodyCallback();
	for(int x=0 ; x<3 ; x++) {
		for(int y=0 ; y<3 ; y++) {
			for(int z=0 ; z<3 ; z++) {
				osg::PositionAttitudeTransform * pat = new osg::PositionAttitudeTransform();
				pat->setUserData(new bodyDataType(fallShape,
				                                 x,
				                                 y,
				                                 z));
				pat->setUpdateCallback(bodyCB);
				pat->addChild(boxGeode);
				root->addChild(pat);
			}
		}
	}

	// Make the viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	// Clean Bullet /////////////////////////////////////////////////////////////////////
	//			dynamicsWorld->removeRigidBody(fallRigidBodies[x][y][z]);
	//			delete fallRigidBodies[x][y][z]->getMotionState();
	//			delete fallRigidBodies[x][y][z];
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
