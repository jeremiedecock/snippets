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
    osg::ref_ptr<osg::Box> box = new osg::Box( osg::Vec3(0,0,0), 1.0f );
    osg::ref_ptr<osg::Capsule> capsule = new osg::Capsule( osg::Vec3(3,0,0), 1.0f, 3.0f );
    osg::ref_ptr<osg::Cone> cone = new osg::Cone( osg::Vec3(6,0,0), 1.0f, 3.0f );
    osg::ref_ptr<osg::Cylinder> cylinder = new osg::Cylinder( osg::Vec3(9,0,0), 1.0f, 3.0f );
    osg::ref_ptr<osg::Sphere> sphere = new osg::Sphere( osg::Vec3(12,0,0), 1.0f );

    osg::ref_ptr<osg::ShapeDrawable> boxDrawable = new osg::ShapeDrawable(box);
    osg::ref_ptr<osg::ShapeDrawable> capsuleDrawable = new osg::ShapeDrawable(capsule);
    osg::ref_ptr<osg::ShapeDrawable> coneDrawable = new osg::ShapeDrawable(cone);
    osg::ref_ptr<osg::ShapeDrawable> cylinderDrawable = new osg::ShapeDrawable(cylinder);
    osg::ref_ptr<osg::ShapeDrawable> sphereDrawable = new osg::ShapeDrawable(sphere);

    osg::ref_ptr<osg::Geode> geodeBox = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeCapsule = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeCone = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeCylinder = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeSphere = new osg::Geode();

    geodeBox->addDrawable(boxDrawable);
    geodeCapsule->addDrawable(capsuleDrawable);
    geodeCone->addDrawable(coneDrawable);
    geodeCylinder->addDrawable(cylinderDrawable);
    geodeSphere->addDrawable(sphereDrawable);

    osg::ref_ptr<osg::Group> root = new osg::Group();
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
