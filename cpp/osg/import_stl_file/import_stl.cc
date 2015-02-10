/* 
 * Import and render an object form a STL file.
 *
 * Copyright (c) 2015 Jérémie Decock
 *
 * See: "OpenSceneGraph 3.0 Beginner's Guide" chap. 10
 */

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

int main(int, char **) {

    osg::ref_ptr<osg::Node> node = osgDB::readNodeFile("object.stl");

    osg::ref_ptr<osg::Group> root = new osg::Group;
    root->addChild(node);

    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
