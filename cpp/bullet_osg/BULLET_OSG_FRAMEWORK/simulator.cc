/* 
 * Bullet OSG Framework.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#include "box.h"
#include "bullet_environment.h"
#include "ground.h"
#include "osg_environment.h"
#include "part.h"
#include "tools.h"

#include <vector>
#include <iostream>

#include <Eigen/Dense>

// TODO:
// x Utiliser eigen pour les vecteur donnés aux constructeurs des Objets
// x MSAA
// x Black background
// x Light (directional ?)
// x Ajouter et utiliser asseseurs dans Objects
// x Ajouter des fonctions wrapper vec3_eigen_to_bullet, ...
// x Renommer Objects -> Parts
// x Séparer les modules
// - Ombres
// - Key reset
// - Key take screenshot
// - Key start/stop recording -> screencast
// - Faire des vidéos et les poster sur jdhp
// - Permettre de configurer le refresh rate ou de passer en mode "temps réel" (-1)
// - Scale units factor (mm ?, kg ?, ...)
// - Ajouter des objets: sphere, cylindre, etc.
// - Objets STL
// - Améliorer l'objet "Ground" + fog + LOD
//
// - Logs (JSON ?)
// - Permettre de lancer une simulation sans interface graphique (sans osg) -> permetter de remplacer le "physicsCallback"
//
// - Remplacer le makefile par un cmakelist
// - Créer une arborescence et des modules .h/.cpp
//
// - Vérifier à la main une simulation simple (calculer à la main l'équation d'un objet qui tombe et comparer avec bullet)
//
// - Singleton OSG / Bullet ? -> bof...
// - Caméra
// - Hinges
// - Commandes d'entrée pour hinge
// - Txt infos (hinge constraints, ...)


int main(int, char **) {

    // Init Bullet //////////////////////////////////////////////////////////////////////

    std::vector<simulator::Part *> * objects_vec = new std::vector<simulator::Part *>;
    objects_vec->push_back(new simulator::Ground());
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 20.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(1., 0., 5.), Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 3., 1.), Eigen::Vector3d(0., 0., 30.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(2., 2., 2.), Eigen::Vector3d(0., 0., 40.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 3.));
    objects_vec->push_back(new simulator::Box(Eigen::Vector3d(1., 1., 1.), Eigen::Vector3d(0., 0., 50.), Eigen::Vector4d(0., 0., 0., 1.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), Eigen::Vector3d(0., 0., 0.), 1.));

    simulator::BulletEnvironment * bullet_environment = new simulator::BulletEnvironment(objects_vec);

    // Init OSG /////////////////////////////////////////////////////////////////////////

    simulator::OSGEnvironment * osg_environment = new simulator::OSGEnvironment(bullet_environment, objects_vec);

    // Run the simulation ///////////////////////////////////////////////////////////////
    
    osg_environment->run();

    // Clean Bullet /////////////////////////////////////////////////////////////////////

    delete bullet_environment;
    delete osg_environment;
    // TODO: delete object_vec and its contents

    return 0;
}
