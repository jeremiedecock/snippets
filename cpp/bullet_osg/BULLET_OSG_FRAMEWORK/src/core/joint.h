/* 
 * Bullet OSG Framework.
 * Joint module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_JOINT_H
#define BOTSIM_JOINT_H

#include <string>

#include <btBulletDynamicsCommon.h>

namespace simulator {

    class Joint {
        protected:
            // Bullet
            btTypedConstraint * bulletTypedConstraint;

        public:
            virtual ~Joint() {};

            // Bullet accessors (return bullet objects) ///////////////////////////////////////////

            btTypedConstraint * getBulletTypedConstraint() const;

            // Misc
            
            virtual std::string getName() const = 0;
    };

}

#endif // BOTSIM_JOINT_H
