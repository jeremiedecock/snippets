/* 
 * Bullet OSG Framework.
 * The robudog controller module.
 *
 * Copyright (c) 2015 Jérémie Decock <jd.jdhp@gmail.com>
 *
 * www.jdhp.org
 */

#ifndef BOTSIM_ROBUDOG_CONTROLLER_H
#define BOTSIM_ROBUDOG_CONTROLLER_H

#include "controller.h"

namespace simulator {

    class RobudogController: public simulator::Controller {
        protected:
            // Common
            double amplitude;  // The peak deviation of the function from zero.
            double frequency;  // The number of oscillations (cycles) that occur each second of time.
            double phase;      // Specifies (in radians) where in its cycle the oscillation is at t = 0.
            std::string name;  // The name of this instance.

        public:
            /**
             * A very basic controler wich sends a sinusoidal signal to actuators.
             * It only requires a Clock (time) sensor.
             * The signal "y" sent to actuators with respect to time is:
             *
             * y(t) = amplitude * sin(2.0 * PI * frequency * t + phase)
             *
             * \param[in] amplitude  The peak deviation of the function from zero.
             * \param[in] frequency  The number of oscillations (cycles) that occur each second of time.
             * \param[in] phase      Specifies (in radians) where in its cycle the oscillation is at t = 0.
             * \param[in] name       The name of this instance.
             */
            RobudogController(std::set<simulator::Actuator *> actuator_set,
                             std::set<simulator::Sensor *> sensor_set,
                             double _amplitude,
                             double _frequency,
                             double _phase,
                             std::string _name="");

            ~RobudogController();

            double computeSignalValue(double time) const;

            void updateActuators();

            double getAmplitude() const;

            double getFrequency() const;

            double getPhase() const;

            std::string getName() const;
    };

}

#endif // BOTSIM_ROBUDOG_CONTROLLER_H
