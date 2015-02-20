/* 
 * OSG Colors
 *
 * Copyright (c) 2015 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osgViewer/Viewer>

int main(int, char **) {

    // Set scenegraph
    osg::ref_ptr<osg::Box> box1 = new osg::Box( osg::Vec3(-5,0,0), 1.0f );
    osg::ref_ptr<osg::Box> box2 = new osg::Box( osg::Vec3(0,0,0), 1.0f );
    osg::ref_ptr<osg::Box> box3 = new osg::Box( osg::Vec3(5,0,0), 1.0f );

    osg::ref_ptr<osg::ShapeDrawable> boxDrawable1 = new osg::ShapeDrawable(box1);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawable2 = new osg::ShapeDrawable(box2);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawable3 = new osg::ShapeDrawable(box3);

    boxDrawable1->setColor(osg::Vec4(1.0f, 0.0f, 0.0f, 0.0f));
    boxDrawable2->setColor(osg::Vec4(0.0f, 1.0f, 0.0f, 0.0f));
    boxDrawable3->setColor(osg::Vec4(0.0f, 0.0f, 1.0f, 0.0f));

    osg::ref_ptr<osg::Geode> geodeBox1 = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeBox2 = new osg::Geode();
    osg::ref_ptr<osg::Geode> geodeBox3 = new osg::Geode();

    geodeBox1->addDrawable(boxDrawable1);
    geodeBox2->addDrawable(boxDrawable2);
    geodeBox3->addDrawable(boxDrawable3);

    osg::ref_ptr<osg::Group> root = new osg::Group();
    root->addChild(geodeBox1);
    root->addChild(geodeBox2);
    root->addChild(geodeBox3);

    // Viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
