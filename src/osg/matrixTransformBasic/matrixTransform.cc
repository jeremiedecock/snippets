/* 
 * OSG Position Attitude Transform
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/MatrixTransform>
#include <osgViewer/Viewer>
#include <osg/Matrix>

int main(int, char **) {
	// Set scenegraph
	osg::Box* cube = new osg::Box( osg::Vec3(0,0,0), 1.0f );

	osg::ShapeDrawable* cubeDrawable = new osg::ShapeDrawable(cube);

	osg::Geode* geode = new osg::Geode();
	geode->addDrawable(cubeDrawable);

	osg::MatrixTransform* mt = new osg::MatrixTransform();
	mt->addChild(geode);

	osg::Group* root = new osg::Group();
	root->addChild(geode);			// the first cube
	root->addChild(mt);			// the second cube

	// Setup Transform
	osg::Matrix m;
	m.setTrans(5,0,0);
	mt->setMatrix(m);

	// Viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	return 0;
}
