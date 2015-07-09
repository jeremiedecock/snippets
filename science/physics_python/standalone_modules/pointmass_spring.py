#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2015 Jérémie DECOCK (http://www.jdhp.org)

import numpy as np


class State:
    def __init__(self, ndim):
        self.ndim = ndim
        self.position = np.zeros(self.ndim)
        self.velocity = np.zeros(self.ndim)


class Model:

    def __init__(self, mass=1., stiffness=1.):

        self.mass = mass
        self.stiffness = stiffness


    def compute_acceleration(self, state):

        # F = -k.x
        self.stretch = state.position[0]  # 0 is the "rest" point
        total_external_force = -1. * self.stiffness * self.stretch

        # a = f/m
        acceleration = total_external_force / self.mass

        return acceleration


def compute_new_state(state, acceleration, delta_time):
    "Compute the forward kinematics with finite difference method."

    new_state = State(state.ndim)
    
    # Velocity (m/s) at time_n+1
    new_state.velocity = state.velocity + acceleration * delta_time

    # Position (m) at time_n+1
    new_state.position = state.position + state.velocity * delta_time

    return new_state


def main():

    state = State(ndim=1)
    state.position[0] = 1.  # initial stiffness (0 is the "rest" point)

    time = 0.
    delta_time = 0.01

    model = Model()

    print("#time  acceleration  velocity  position")

    while time < 12:

        time = time + delta_time

        # Update state (physics)
        acceleration = model.compute_acceleration(state)
        state = compute_new_state(state, acceleration, delta_time)

        print(time, acceleration, state.velocity[0], state.position[0])


if __name__ == "__main__":
    main()

