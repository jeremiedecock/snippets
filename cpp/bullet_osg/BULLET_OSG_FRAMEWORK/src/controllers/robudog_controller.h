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

#include <Eigen/Dense>

namespace simulator {

    class RobudogController: public simulator::Controller {
        protected:
            /*
             * Parameters of the controler.
             *
             * This vector contains a tuple of 3 parameters for each of the 8
             * actuators and is defined like this:
             *
             *    parameter = (a1, f1, p1, a2, f2, p2, ... , a8, f8, p8),
             *
             * where:
             * - 'ai' is the amplitude of the actuator 'i' i.e. the peak
             *   deviation of the function from zero;
             * - 'fi' is the frequency of the actuator 'i' i.e. the number of
             *   oscillations (or cycles) that occur each second of
             *   (simulation) time;
             * - 'pi' is the phase of the actuator 'i' i.e. specifies (in
             *   radians) where in its cycle the oscillation is at t=0.
             *
             * and where:
             * - actuator1 is the "right_shoulder_motor";
             * - actuator2 is the "left_shoulder_motor";
             * - actuator3 is the "right_elbow_motor";
             * - actuator4 is the "left_elbow_motor".
             * - actuator5 is the "right_hip_motor";
             * - actuator6 is the "left_hip_motor";
             * - actuator7 is the "right_knee_motor";
             * - actuator8 is the "left_knee_motor".
             */
            Eigen::Matrix< double, 24, 1> parameters;

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
                             Eigen::Matrix< double, 24, 1> _parameters,
                             std::string _name="");

            ~RobudogController();

            double computeSignalValue(double time, double amplitude, double frequency, double phase) const;

            void updateActuators();

            Eigen::Matrix< double, 24, 1> getParameters() const;

            std::string getName() const;
    };

}

#endif // BOTSIM_ROBUDOG_CONTROLLER_H
