/* 
 * OSG Shapes
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osgViewer/Viewer>

int main(int, char **) {

	// Set scenegraph
	osg::Box* box = new osg::Box( osg::Vec3(0,0,0), 1.0f );
	osg::Capsule* capsule = new osg::Capsule( osg::Vec3(3,0,0), 1.0f, 3.0f );
	osg::Cone* cone = new osg::Cone( osg::Vec3(6,0,0), 1.0f, 3.0f );
	osg::Cylinder* cylinder = new osg::Cylinder( osg::Vec3(9,0,0), 1.0f, 3.0f );
	osg::Sphere* sphere = new osg::Sphere( osg::Vec3(12,0,0), 1.0f );

	osg::ShapeDrawable* boxDrawable = new osg::ShapeDrawable(box);
	osg::ShapeDrawable* capsuleDrawable = new osg::ShapeDrawable(capsule);
	osg::ShapeDrawable* coneDrawable = new osg::ShapeDrawable(cone);
	osg::ShapeDrawable* cylinderDrawable = new osg::ShapeDrawable(cylinder);
	osg::ShapeDrawable* sphereDrawable = new osg::ShapeDrawable(sphere);

	osg::Geode* geodeBox = new osg::Geode();
	osg::Geode* geodeCapsule = new osg::Geode();
	osg::Geode* geodeCone = new osg::Geode();
	osg::Geode* geodeCylinder = new osg::Geode();
	osg::Geode* geodeSphere = new osg::Geode();

	geodeBox->addDrawable(boxDrawable);
	geodeCapsule->addDrawable(capsuleDrawable);
	geodeCone->addDrawable(coneDrawable);
	geodeCylinder->addDrawable(cylinderDrawable);
	geodeSphere->addDrawable(sphereDrawable);

	osg::Group* root = new osg::Group();
	root->addChild(geodeBox);
	root->addChild(geodeCapsule);
	root->addChild(geodeCone);
	root->addChild(geodeCylinder);
	root->addChild(geodeSphere);

	// Viewer
	osgViewer::Viewer viewer;
	viewer.setSceneData(root);
	viewer.run();

	return 0;
}
