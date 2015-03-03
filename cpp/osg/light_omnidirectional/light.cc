/* 
 * OSG Simple sphere with a light and materials.
 *
 * Copyright (c) 2009,2015 Jérémie Decock
 *
 * See the very good tutorial http://jeux.developpez.com/tutoriels/openscenegraph/lumiere/
 */

#include <osg/Group>
#include <osg/Geode>
#include <osg/ShapeDrawable>
#include <osg/Material>
#include <osgViewer/Viewer>

int main(int, char **) {

    // SET SCENEGRAPH ///////
    
    osg::ref_ptr<osg::Sphere> sphere1 = new osg::Sphere( osg::Vec3( 3, 3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere2 = new osg::Sphere( osg::Vec3( 3,-3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere3 = new osg::Sphere( osg::Vec3(-3, 3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere4 = new osg::Sphere( osg::Vec3(-3,-3,0), 1.0f );
    osg::ref_ptr<osg::Box> box = new osg::Box( osg::Vec3(0,0,-3), 1.0f );
    box->setHalfLengths(osg::Vec3(17, 17, 0.2));

    osg::ref_ptr<osg::ShapeDrawable> boxDrawableSphere1 = new osg::ShapeDrawable(sphere1);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawableSphere2 = new osg::ShapeDrawable(sphere2);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawableSphere3 = new osg::ShapeDrawable(sphere3);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawableSphere4 = new osg::ShapeDrawable(sphere4);
    osg::ref_ptr<osg::ShapeDrawable> boxDrawableBox = new osg::ShapeDrawable(box);

    osg::ref_ptr<osg::Geode> geodeSphere1 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere2 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere3 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere4 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeBox = new osg::Geode;

    geodeSphere1->addDrawable(boxDrawableSphere1);
    geodeSphere2->addDrawable(boxDrawableSphere2);
    geodeSphere3->addDrawable(boxDrawableSphere3);
    geodeSphere4->addDrawable(boxDrawableSphere4);
    geodeBox->addDrawable(boxDrawableBox);

    osg::ref_ptr<osg::Group> root = new osg::Group;
    root->addChild(geodeSphere1);
    root->addChild(geodeSphere2);
    root->addChild(geodeSphere3);
    root->addChild(geodeSphere4);
    root->addChild(geodeBox);


    // LIGHT ////////////////

    osg::ref_ptr<osg::Light> light = new osg::Light;

    // OSG (as OpenGL) can handle up to 8 light sources.
    // Each light must have a unique number
    //
    // Light number 0 is the default one (integrated to the camera).
    //
    // We do not use light number 0, because we do not want to override the OSG
    // default headlights.
    light->setLightNum(1);

    //light->setAmbient(osg::Vec4(0.0, 0.0, 1.0, 1.0));
    //light->setDiffuse(osg::Vec4(1.0, 0.0, 0.0, 1.0));
    //light->setSpecular(osg::Vec4(0.0, 1.0, 0.0, 1.0));

    light->setAmbient(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    light->setDiffuse(osg::Vec4(1.0, 1.0, 1.0, 0.0));
    light->setSpecular(osg::Vec4(1.0, 1.0, 1.0, 1.0));

    // The light's position
    light->setPosition(osg::Vec4(3.0, 3.0, 3.0, 1.0)); // last param w = 0.0 directional light (direction)
                                                       // w = 1.0 point light (position or omnidirectional)

    // Light source
    osg::ref_ptr<osg::LightSource> light_source = new osg::LightSource;    
    light_source->setLight(light);
    root->addChild(light_source);

    // Modify the StateSet for the root node i.e. a StateSet shared and applied
    // to all nodes (see http://www.sm.luth.se/csee/courses/smm/011/l/t2.pdf slide 35)
    osg::ref_ptr<osg::StateSet> state = root->getOrCreateStateSet();
    state->setMode(GL_LIGHT0, osg::StateAttribute::OFF); // GL_LIGHT0 is the default light
    state->setMode(GL_LIGHT1, osg::StateAttribute::ON);  // use GL_LIGHTN for light number N


    // Material
    osg::ref_ptr<osg::Material> mat = new osg::Material;
    mat->setDiffuse(osg::Material::FRONT, osg::Vec4(.0f, 1.0f, .0f, 1.f)); // the diffuse color of the material
    mat->setSpecular(osg::Material::FRONT, osg::Vec4(1.f, 1.f, 1.f, 0.f)); // the specular color of the material
    mat->setShininess(osg::Material::FRONT, 96.f);
    state->setAttribute(mat.get()); 


    // VIEWER ///////////////
    
    osgViewer::Viewer viewer;
    viewer.getCamera()->setClearColor(osg::Vec4(0.0f, 0.0f, 0.0f, 0.0f));  // change the background color (black)
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
