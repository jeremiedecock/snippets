/* 
 * OSG Position Attitude Transform
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>
#include <osg/Vec3>

int main(int, char **) {

	// Set scenegraph
	osg::Box* cube = new osg::Box( osg::Vec3(0,0,0), 1.0f );

	osg::ShapeDrawable* cubeDrawable = new osg::ShapeDrawable(cube);

	osg::Geode* geode = new osg::Geode();
	geode->addDrawable(cubeDrawable);

	osg::PositionAttitudeTransform* pat = new osg::PositionAttitudeTransform();
	pat->addChild(geode);

	osg::Group* root = new osg::Group();
	root->addChild(geode);			// the first cube
	root->addChild(pat);			// the second cube

	// Set Position Attitude Transform
	osg::Vec3 vectTrans(5,0,0);
	pat->setPosition(vectTrans);

	// Viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	return 0;
}
