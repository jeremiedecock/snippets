/* 
 * Import and render an object form a STL file.
 *
 * This snippet shows that OpenSceneGraph and OpenSCAL use the same scale. 
 * This shows that 1 unit in OpenSceneGraph = 1 unit in OpenSCAL (= 1mm in 3D printers).
 *
 * Copyright (c) 2015 Jérémie Decock
 *
 * See: "OpenSceneGraph 3.0 Beginner's Guide" chap. 10
 */

#include <osg/Geode>
#include <osg/Group>
#include <osg/ShapeDrawable>
#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

int main(int, char **) {

    // Create an object of 10mm height and 5mm width and 5mm depth.
    osg::ref_ptr<osg::Node> node = osgDB::readNodeFile("object.stl");
    
    // Create an object of 5mm height and 5mm width and 5mm depth and translate
    // it 10mm on the x axis.
    osg::ref_ptr<osg::Box> box = new osg::Box( osg::Vec3(10,0,0), 5.0f );

    osg::ref_ptr<osg::ShapeDrawable> boxDrawable = new osg::ShapeDrawable(box);

    osg::ref_ptr<osg::Geode> geodeBox = new osg::Geode();
    geodeBox->addDrawable(boxDrawable);

    osg::ref_ptr<osg::Group> root = new osg::Group;
    root->addChild(node);
    root->addChild(geodeBox);

    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
