/* 
 * OSG Model
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

int main(int, char **) {
    osg::ref_ptr<osg::Node> model = osgDB::readNodeFile("cessna.osg"); // could be also .obj files, ...

    osgViewer::Viewer viewer;
    viewer.setSceneData(model);
    viewer.run();

    return 0;
}
