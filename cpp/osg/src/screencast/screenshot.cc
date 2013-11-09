/*
 * 2013 Jérémie Decock
 *
 * Inspired by /usr/share/openscenegraph/examples/osgautocapture/osgautocapture.cpp (from "openscenegraph-examples" Debian package)
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/PositionAttitudeTransform>

#include <osgViewer/Viewer>

#include <osgDB/WriteFile>

#include <iostream>
#include <sstream>
#include <iomanip>

const std::string FILENAME("capture");
const std::string FILE_EXTENSION("png");

/**
 * Capture the frame buffer and write image to disk
 */
class WindowCaptureCallback : public osg::Camera::DrawCallback
{
    protected:

    GLenum                      _readBuffer;
    osg::ref_ptr<osg::Image>    _image;
    mutable OpenThreads::Mutex  _mutex;
    mutable unsigned int        _frameId;

    public:

    /**
     *
     */
    WindowCaptureCallback(GLenum readBuffer) : _readBuffer(readBuffer) {
        _image = new osg::Image;
        _frameId = 0;
    }
    
    /**
     *
     */
    virtual void operator () (osg::RenderInfo& renderInfo) const {
        OpenThreads::ScopedLock<OpenThreads::Mutex> lock(_mutex);
        osg::GraphicsContext* gc = renderInfo.getState()->getGraphicsContext();
        if (gc->getTraits()) {
            GLenum pixelFormat;

            if (gc->getTraits()->alpha)
                pixelFormat = GL_RGBA;
            else 
                pixelFormat = GL_RGB;

            int width = gc->getTraits()->width;
            int height = gc->getTraits()->height;

            std::cout << "Capture: size=" << width << "x" << height << ", format=" << (pixelFormat == GL_RGBA ? "GL_RGBA":"GL_RGB") << std::endl;

            _image->readPixels(0, 0, width, height, pixelFormat, GL_UNSIGNED_BYTE);
        }

        _frameId++;

        std::ostringstream oss;
        oss << FILENAME << "_" << std::setfill('0') << std::setw(4) <<  _frameId << "." << FILE_EXTENSION;
        std::string filename(oss.str());

        std::cout << "Writing to: " << filename << std::endl;
        osgDB::writeImageFile(*_image, filename);
    }
};


int main(int, char **) {
    // Make the scene graph
    osg::ref_ptr<osg::Box> box = new osg::Box(osg::Vec3(0, 0, 0), 1.0f);

    osg::ref_ptr<osg::ShapeDrawable> sd = new osg::ShapeDrawable(box);

    osg::ref_ptr<osg::Geode> geode = new osg::Geode();
    geode->addDrawable(sd);

    osg::ref_ptr<osg::PositionAttitudeTransform> pat1 = new osg::PositionAttitudeTransform();
    pat1->addChild(geode);

    osg::ref_ptr<osg::Group> root = new osg::Group();
    root->addChild(pat1);
    
    // Setup PAT
    pat1->setAttitude(osg::Quat(0, osg::Vec3(1,0,0),
                                20, osg::Vec3(0,1,0),
                                20, osg::Vec3(0,0,1)));

    // Make the viewer
    osgViewer::Viewer viewer;
    viewer.setSceneData(root);

    // Setup the camera
    osg::Matrix trans;
    osg::Matrix rot;
    trans.makeTranslate(0., 0., -10.);
    viewer.getCamera()->setViewMatrix(trans * rot); 

    // Render one frame to avoid segfault in next lines
    viewer.frame();

    // Set callback to get screenshots
    GLenum buffer = viewer.getCamera()->getGraphicsContext()->getTraits()->doubleBuffer ? GL_BACK : GL_FRONT;
    viewer.getCamera()->setFinalDrawCallback(new WindowCaptureCallback(buffer));

    //viewer.run();
    double angle(0.);
    while(!viewer.done()) {

        angle += 0.01;
        pat1->setAttitude(osg::Quat(angle * .5,     osg::Vec3(1,0,0),
                                    angle * 1., osg::Vec3(0,1,0),
                                    angle * 2., osg::Vec3(0,0,1)));

        viewer.frame();
    }

    return 0;
}
