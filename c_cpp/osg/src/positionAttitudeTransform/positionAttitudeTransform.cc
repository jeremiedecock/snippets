#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

int main(int, char **) {
	// Make the scene graph
	osg::Box *box = new osg::Box(osg::Vec3(0, 0, 0), 1.0f);

	osg::ShapeDrawable *sd = new osg::ShapeDrawable(box);

	osg::Geode *geode = new osg::Geode();
	geode->addDrawable(sd);

	osg::PositionAttitudeTransform *pat1 = new osg::PositionAttitudeTransform();
	pat1->addChild(geode);

	osg::PositionAttitudeTransform *pat2 = new osg::PositionAttitudeTransform();
	pat2->addChild(geode);

	osg::Group *root = new osg::Group();
	root->addChild(pat1);
	root->addChild(pat2);

	// Setup PAT
	pat1->setPosition(osg::Vec3(2,0,0));
	pat1->setAttitude(osg::Quat(
				0, osg::Vec3(1,0,0),
				20, osg::Vec3(0,1,0),
				20, osg::Vec3(0,0,1)));

	pat2->setAttitude(osg::Quat(20, osg::Vec3(0,1,0)));

	// Make the viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	return 0;
}
