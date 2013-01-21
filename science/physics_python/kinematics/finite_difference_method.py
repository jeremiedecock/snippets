# -*- coding: utf-8 -*-

# Copyright (c) 2010 Jérémie DECOCK (http://www.jdhp.org)

from common.state import State

name = 'Finite difference method'

class Kinematics:

    def __init__(self):
        pass

    def compute_new_state(self, state, acceleration, delta_time):
        "Compute the forward kinematics with finite difference method."

        new_state = State(state.ndim)
        
        # Velocity (m/s) at time_n+1
        new_state.velocity = state.velocity + acceleration * delta_time

        # Position (m) at time_n+1
        new_state.position = state.position + state.velocity * delta_time
        #new_state.position = state.position + new_state.velocity * delta_time

        return new_state
