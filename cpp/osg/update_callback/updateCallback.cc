#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>
#include <osgViewer/Viewer>

class RotateCB : public osg::NodeCallback {
    protected :

    double _angle;

    public :

    RotateCB() : _angle(0.) {}

    virtual void operator() (osg::Node * node, osg::NodeVisitor * nv) {
        _angle += 0.01;

        osg::PositionAttitudeTransform * pat = dynamic_cast<osg::PositionAttitudeTransform*> (node);
        pat->setAttitude(osg::Quat(_angle, osg::Vec3(0, 1, 0)));

        traverse(node, nv);
    }
};

int main(int, char **) {

    // Make the scene graph
    osg::ref_ptr<osg::Box> box = new osg::Box(osg::Vec3(0, 0, 0), 1.0f);

    osg::ref_ptr<osg::ShapeDrawable> sd = new osg::ShapeDrawable(box);

    osg::ref_ptr<osg::Geode> geode = new osg::Geode();
    geode->addDrawable(sd);

    osg::ref_ptr<osg::PositionAttitudeTransform> pat = new osg::PositionAttitudeTransform();
    pat->addChild(geode);

    osg::ref_ptr<osg::Group> root = new osg::Group();
    root->addChild(pat);

    // Setup Transform
    pat->setPosition(osg::Vec3(2, 0, 0));
    pat->setUpdateCallback(new RotateCB);

    // Make the viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
