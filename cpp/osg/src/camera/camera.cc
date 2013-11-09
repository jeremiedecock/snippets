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

    viewer.getCamera()->setProjectionMatrixAsPerspective(40., 1., 1., 100.);

    osg::Matrix trans;
    osg::Matrix rot;

    double angle(0.);
    while(!viewer.done()) {
        trans.makeTranslate(0., 0., -40 - angle);
        rot.makeRotate(angle, osg::Vec3(0., 0., 1.));
        angle += 0.01;

        viewer.getCamera()->setViewMatrix(trans * rot); 

        viewer.frame();
    }

    return 0;
}
