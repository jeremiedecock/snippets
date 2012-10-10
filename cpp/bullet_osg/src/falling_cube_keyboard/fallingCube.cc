#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

#include <btBulletDynamicsCommon.h>

btCollisionShape * fallShape;
btRigidBody * fallRigidBody;
btDiscreteDynamicsWorld * dynamicsWorld;

void init(void) {
	btScalar mass = 1;
	btVector3 fallInertia(0, 0, 0);
	fallShape->calculateLocalInertia(mass, fallInertia);

	btDefaultMotionState * fallMotionState = new btDefaultMotionState(btTransform(btQuaternion(1,1,1,25),
	                                                                              btVector3(0,0,20)));
	btRigidBody::btRigidBodyConstructionInfo fallRigidBodyCI(mass,
	                                                         fallMotionState,
	                                                         fallShape,
	                                                         fallInertia);
	dynamicsWorld->removeRigidBody(fallRigidBody);
	delete(fallRigidBody);
	fallRigidBody = new btRigidBody(fallRigidBodyCI);
	dynamicsWorld->addRigidBody(fallRigidBody);
}

class myKeyboardEventHandler : public osgGA::GUIEventHandler {
	public:
		virtual bool handle(const osgGA::GUIEventAdapter& ea,osgGA::GUIActionAdapter&);

		virtual void accept(osgGA::GUIEventHandlerVisitor& v) {
			v.visit(*this);
		};
};

bool myKeyboardEventHandler::handle(const osgGA::GUIEventAdapter& ea, osgGA::GUIActionAdapter& aa) {
	switch(ea.getEventType()) {
		case(osgGA::GUIEventAdapter::KEYDOWN): 	{
				switch(ea.getKey()) {
					case 'i':
						init();
						return false;
						break;
					default:
						return false;
				} 
			}
		default:
			return false;
	}
}

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
	fallShape = new btBoxShape(btVector3(0.5, 0.5, 0.5)); // ce sont des half lengths

	// Ground
	btDefaultMotionState * groundMotionState = new btDefaultMotionState(btTransform(btQuaternion(0,0,0,1),
	                                                                                btVector3(0,0,0)));
	btRigidBody::btRigidBodyConstructionInfo groundRigidBodyCI(0,
	                                                           groundMotionState,
	                                                           groundShape,
	                                                           btVector3(0, 0, 0));
	btRigidBody* groundRigidBody = new btRigidBody(groundRigidBodyCI);

	// Box
	btScalar mass = 1;
	btVector3 fallInertia(0, 0, 0);
	fallShape->calculateLocalInertia(mass, fallInertia);

	btDefaultMotionState * fallMotionState = new btDefaultMotionState(btTransform(btQuaternion(1,1,1,25),
	                                                                              btVector3(0,0,20)));
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
	osg::Box * box = new osg::Box(osg::Vec3(0, 0, 0), 1.0f);
	osg::Box * ground = new osg::Box(osg::Vec3(0, 0, -1), 1.0f);
	ground->setHalfLengths(osg::Vec3(15, 15, 1));

	osg::ShapeDrawable * boxSd = new osg::ShapeDrawable(box);
	osg::ShapeDrawable * groundSd = new osg::ShapeDrawable(ground);

	osg::Geode * boxGeode = new osg::Geode();
	osg::Geode * groundGeode = new osg::Geode();
	boxGeode->addDrawable(boxSd);
	groundGeode->addDrawable(groundSd);

	osg::PositionAttitudeTransform * boxPat = new osg::PositionAttitudeTransform();
	boxPat->setUpdateCallback(new BulletCB);
	boxPat->addChild(boxGeode);

	osg::Group * root = new osg::Group();
	root->addChild(groundGeode);
	root->addChild(boxPat);

	// Make the viewer
	osgViewer::Viewer viewer;
	
	myKeyboardEventHandler* myEventHandler = new myKeyboardEventHandler();
	viewer.addEventHandler(myEventHandler); 

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
