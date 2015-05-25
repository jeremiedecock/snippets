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

namespace botsim {

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

        protected:
            /**
             * Forbid instantiation.
             */
            Joint() {};      // TODO ?

        private:
            /**
             * Forbid copy of instances.
             */
            Joint(const Joint &);

            /**
             * Forbid assignment.
             */
            Joint & operator = (const Joint &);
    };

}

#endif // BOTSIM_JOINT_H
