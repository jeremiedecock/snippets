#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

# See:
# - http://www.ferdinandpiette.com/blog/2011/08/implementer-un-pid-sans-faire-de-calculs/
# - http://www.f3c-f3n.fr/le-pid-pour-les-nuls-1/
# - https://fr.wikipedia.org/wiki/R%C3%A9gulateur_PID
# - http://code.activestate.com/recipes/577231-discrete-pid-controller/
# - https://en.wikipedia.org/wiki/PID_controller
# - http://www.rhaaa.fr/regulation-pid-comment-la-regler-12
# - http://www.energieplus-lesite.be/index.php?id=11247

import argparse

import numpy as np
import matplotlib.pyplot as plt

################################################################################

class State(object):
    def __init__(self):
        self.position = 0
        self.velocity = 0

################################################################################

class Model(object):
    def computeNextState(self, state, control):
        raise NotImplementedError

    def forwardKinematicsFunction(self, state, acceleration, delta_time):
        "Compute the forward kinematics with finite difference method."

        new_state = State()
        
        # Velocity (m/s) at time_n+1
        new_state.velocity = state.velocity + acceleration * delta_time

        # Position (m) at time_n+1
        new_state.position = state.position + state.velocity * delta_time

        return new_state


class PointMassModel(Model):
    def __init__(self, mass=1.):
        self.mass = mass

    def computeNextState(self, state, control, delta_time):
        # F = u
        total_external_force = control

        # a = f/m
        acceleration = total_external_force / self.mass

        # compute velocity and position
        state = self.forwardKinematicsFunction(state, acceleration, delta_time)

        return state


class PointMassModelWithKineticFriction(Model):
    def __init__(self, mass=1.):
        self.mass = mass

    def computeNextState(self, state, control, delta_time):
        # F = u
        total_external_force = control - state.velocity

        # a = f/m
        acceleration = total_external_force / self.mass

        # compute velocity and position
        state = self.forwardKinematicsFunction(state, acceleration, delta_time)

        return state

################################################################################

class Controller(object):
    def computeControl(self, state):
        raise NotImplementedError


class PID(Controller):
    def __init__(self, target_state, p_factor, i_factor=0., d_factor=0.):
        self.targetState = target_state

        self.pFactor = p_factor
        self.iFactor = i_factor
        self.dFactor = d_factor

        self.errorSum = 0
        self.previousError = 0

    def computeControl(self, state):
        if (self.targetState.position is not None) and (self.targetState.velocity is None):
            error = self.targetState.position - state.position
        elif (self.targetState.position is None) and (self.targetState.velocity is not None):
            error = self.targetState.velocity - state.velocity
        else:
            raise ValueError("Wrong target_state value.")

        self.errorSum += error
        delta_error = error - self.previousError

        control = self.pFactor * error + self.iFactor * self.errorSum + self.dFactor * delta_error
        
        self.previousError = error

        return control


################################################################################

def main():

    # ARGPARSE ########################

    parser = argparse.ArgumentParser(description='An argparse snippet.')

    parser.add_argument("--p_factor", "-p",  help="TODO", type=float, default=0., metavar="FLOAT")
    parser.add_argument("--i_factor", "-i",  help="TODO", type=float, default=0., metavar="FLOAT")
    parser.add_argument("--d_factor", "-d",  help="TODO", type=float, default=0., metavar="FLOAT")
    parser.add_argument("--experiment", "-x",  help="TODO", type=int, default=0, metavar="INTEGER") # TODO

    args = parser.parse_args()

    p_factor = args.p_factor
    i_factor = args.i_factor
    d_factor = args.d_factor

    # PID #############################

    state = State()
    state.position = 0.
    state.velocity = 0.

    target_state = State()

    if args.experiment == 0: # For xp0, a PD controller should be used
        target_state.position = 10.
        target_state.velocity = None
    else:                    # For xp1, a PI controller should be used
        target_state.position = None
        target_state.velocity = 10.

    time = 0.
    delta_time = 0.01

    if args.experiment == 0:
        model = PointMassModel()
    else:
        model = PointMassModelWithKineticFriction()

    controller = PID(target_state, p_factor, i_factor, d_factor)

    time_list = []
    control_list = []
    velocity_list = []
    position_list = []

    while time < 100:

        time = time + delta_time

        # Update control
        control = controller.computeControl(state)

        # Update state (physics)
        state = model.computeNextState(state, control, delta_time)

        time_list.append(time)
        control_list.append(control)
        velocity_list.append(state.velocity)
        position_list.append(state.position)


    # PLOT ############################

    fig = plt.figure(figsize=(16.0, 10.0))
    ax = fig.add_subplot(111)

    ax.plot(time_list, control_list, "-", label="control")
    ax.plot(time_list, velocity_list, "-", label="velocity")
    if (target_state.position is not None):
        ax.plot(time_list, position_list, "-", label="position")

    if (target_state.position is not None) and (target_state.velocity is None):
        ax.axhline(target_state.position, linewidth=1, color='black', linestyle='--', label="Target (position)")
    elif (target_state.position is None) and (target_state.velocity is not None):
        ax.axhline(target_state.velocity, linewidth=1, color='black', linestyle='--', label="Target (velocity)")
    else:
        raise ValueError("Wrong target_state value.")

    # Title and labels
    ax.set_title("PID {}, {}, {}".format(p_factor, i_factor, d_factor), fontsize=20)
    ax.set_xlabel(r"$time (s)$", fontsize=32)

    # Legend
    ax.legend(loc='lower right', fontsize=20)

    # Save file
    #plt.savefig("test.pdf")

    # Plot
    plt.show()

################################################################################

if __name__ == "__main__":
    main()

