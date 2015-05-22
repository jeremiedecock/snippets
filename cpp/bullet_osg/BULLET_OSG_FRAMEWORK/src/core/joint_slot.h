/* 
 * Bullet OSG Framework.
 * Joint slot module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_JOINT_SLOT_H
#define BOTSIM_JOINT_SLOT_H

namespace simulator {

    class JointSlot {
        public:
            virtual ~JointSlot() {};

        protected:
            /**
             * Forbid instantiation.
             */
            JointSlot() {};   // TODO ?

        private:
            /**
             * Forbid copy of instances.
             */
            JointSlot(const JointSlot &);

            /**
             * Forbid assignment.
             */
            JointSlot & operator = (const JointSlot &);
    };

}

#endif // BOTSIM_JOINT_SLOT_H
