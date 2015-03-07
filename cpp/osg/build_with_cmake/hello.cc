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
#include <osgShadow/ShadowedScene>
#include <osgShadow/ShadowMap>
#include <osgViewer/Viewer>

int main(int, char **) {

    const unsigned int recv_shadow_mask = 0x1;
    const unsigned int cast_shadow_mask = 0x2;

    // SET SCENEGRAPH ///////
    
    osg::ref_ptr<osg::Sphere> sphere1 = new osg::Sphere( osg::Vec3( 3, 3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere2 = new osg::Sphere( osg::Vec3( 3,-3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere3 = new osg::Sphere( osg::Vec3(-3, 3,0), 1.0f );
    osg::ref_ptr<osg::Sphere> sphere4 = new osg::Sphere( osg::Vec3(-3,-3,0), 1.0f );
    osg::ref_ptr<osg::Box> ground = new osg::Box( osg::Vec3(0,0,-3), 1.0f );
    ground->setHalfLengths(osg::Vec3(17, 17, 0.2));

    osg::ref_ptr<osg::ShapeDrawable> drawableSphere1 = new osg::ShapeDrawable(sphere1);
    osg::ref_ptr<osg::ShapeDrawable> drawableSphere2 = new osg::ShapeDrawable(sphere2);
    osg::ref_ptr<osg::ShapeDrawable> drawableSphere3 = new osg::ShapeDrawable(sphere3);
    osg::ref_ptr<osg::ShapeDrawable> drawableSphere4 = new osg::ShapeDrawable(sphere4);
    osg::ref_ptr<osg::ShapeDrawable> drawableBox = new osg::ShapeDrawable(ground);

    osg::ref_ptr<osg::Geode> geodeSphere1 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere2 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere3 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeSphere4 = new osg::Geode;
    osg::ref_ptr<osg::Geode> geodeBox = new osg::Geode;

    geodeSphere1->addDrawable(drawableSphere1);
    geodeSphere2->addDrawable(drawableSphere2);
    geodeSphere3->addDrawable(drawableSphere3);
    geodeSphere4->addDrawable(drawableSphere4);
    geodeBox->addDrawable(drawableBox);

    geodeSphere1->setNodeMask(cast_shadow_mask);
    geodeSphere2->setNodeMask(cast_shadow_mask);
    geodeSphere3->setNodeMask(cast_shadow_mask);
    geodeSphere4->setNodeMask(cast_shadow_mask);
    geodeBox->setNodeMask(recv_shadow_mask);



    osg::ref_ptr<osgShadow::ShadowedScene> root = new osgShadow::ShadowedScene();


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

    osg::ref_ptr<osgShadow::ShadowMap> sm = new osgShadow::ShadowMap;
    sm->setLight(light_source);
    sm->setTextureSize(osg::Vec2s(2048, 2048));
    sm->setTextureUnit(1);

    root->setShadowTechnique(sm.get());
    root->setReceivesShadowTraversalMask(recv_shadow_mask);
    root->setCastsShadowTraversalMask(cast_shadow_mask);


    root->addChild(geodeSphere1);
    root->addChild(geodeSphere2);
    root->addChild(geodeSphere3);
    root->addChild(geodeSphere4);
    root->addChild(geodeBox);


    // VIEWER ///////////////
    
    osgViewer::Viewer viewer;
    viewer.getCamera()->setClearColor(osg::Vec4(0.0f, 0.0f, 0.0f, 0.0f));  // change the background color (black)
    viewer.setSceneData(root);
    viewer.run();

    return 0;
}
