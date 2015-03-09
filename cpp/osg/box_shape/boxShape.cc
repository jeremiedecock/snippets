/* 
 * OSG Simple box
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osgViewer/Viewer>

int main(int, char **) {

    // Set scenegraph
    osg::ref_ptr<osg::Box> p_box = new osg::Box( osg::Vec3(0,0,0), 1.0f );

    osg::ref_ptr<osg::ShapeDrawable> p_box_drawable = new osg::ShapeDrawable(p_box);

    osg::ref_ptr<osg::Geode> p_geode = new osg::Geode;
    p_geode->addDrawable(p_box_drawable);

    osg::ref_ptr<osg::Group> p_root = new osg::Group;
    p_root->addChild(p_geode);

    // Viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(p_root);
    viewer.run();

    return 0;
}
