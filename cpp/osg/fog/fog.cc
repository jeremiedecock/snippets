/* 
 * OSG Fog
 *
 * Copyright (c) 2015 Jérémie Decock
 *
 * See "OpenSceneGraph 3.0" by Rui Wang and Xuelei Qian (ed. Packt publishing 2010) p.134
 *
 * Note that this snippet doesn't work when used with shader based shadow techniques:
 * http://forum.openscenegraph.org/viewtopic.php?t=6228&view=previous
 * http://trac.openscenegraph.org/projects/osg//wiki/Support/ProgrammingGuide/osgShadow
 */

#include <osg/Fog>
#include <osg/Geode>
#include <osg/Group>
#include <osg/ShapeDrawable>
#include <osgViewer/Viewer>

int main(int, char **) {

    // Set scenegraph
    osg::ref_ptr<osg::Box> p_box = new osg::Box( osg::Vec3(0,0,0), 1.0f );
    p_box->setHalfLengths(osg::Vec3(5., 100., 1.));

    osg::ref_ptr<osg::ShapeDrawable> p_box_drawable = new osg::ShapeDrawable(p_box);

    osg::ref_ptr<osg::Geode> p_geode = new osg::Geode;
    p_geode->addDrawable(p_box_drawable);

    osg::ref_ptr<osg::Group> p_root = new osg::Group;
    p_root->addChild(p_geode);

    // Viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(p_root);

    // Set the fog effect
    osg::ref_ptr<osg::Fog> p_fog = new osg::Fog();
    p_fog->setMode(osg::Fog::LINEAR); // The fog opacity is linear from "start" to "end" (other modes available are exponential ones)
    p_fog->setStart(100.0f);          // The fog start at this distance to the camera
    p_fog->setEnd(500.0f);            // The fog is "complete" at this distance to the camera

    p_fog->setColor(viewer.getCamera()->getClearColor()); // The fog color is the same than the one used for the background
    //p_fog->setColor(osg::Vec4(0.0f, 0.0f, 1.0f, 1.0f));

    // Enable the fog effect
    osg::ref_ptr<osg::StateSet> p_state = p_root->getOrCreateStateSet();
    p_state->setAttributeAndModes(p_fog.get());

    // Run OSG
    viewer.run();

    return 0;
}
