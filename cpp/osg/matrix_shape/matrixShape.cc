/* 
 * OSG Matrix
 *
 * Copyright (c) 2009 Jérémie Decock
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>
#include <osg/Vec3>

#define SIZE 10

int main(int, char **) {
    // Set scenegraph
    osg::ref_ptr<osg::Box> boxes[SIZE][SIZE][SIZE];
    osg::ref_ptr<osg::ShapeDrawable> boxesDrawable[SIZE][SIZE][SIZE];
    osg::ref_ptr<osg::Geode> geodes[SIZE][SIZE][SIZE];

    osg::ref_ptr<osg::Group> root = new osg::Group();

    for(int x=0 ; x<SIZE ; x++) {
        for(int y=0 ; y<SIZE ; y++) {
            for(int z=0 ; z<SIZE ; z++) {
                boxes[x][y][z] = new osg::Box( osg::Vec3(x*2,y*2,z*2), 1.0f );

                boxesDrawable[x][y][z] = new osg::ShapeDrawable(boxes[x][y][z]);

                geodes[x][y][z] = new osg::Geode();
                geodes[x][y][z]->addDrawable(boxesDrawable[x][y][z]);

                root->addChild(geodes[x][y][z]);
            }
        }
    }

    // Viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
