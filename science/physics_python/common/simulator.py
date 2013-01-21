# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

from common.state import State

class Simulator:

    def __init__(self, model, kinematics, delta_time=0.01):

        self.model = model
        self.kinematics = kinematics
        self.delta_time = delta_time


    def run(self):
        """The main loop"""

        state = State(1)
        time = 0

        while time < 5:  #TODO

            time = time + self.delta_time

            # Update state (physics)
            acceleration = self.model.compute_acceleration(state)
            state = self.kinematics.compute_new_state(state, acceleration, self.delta_time)

            print time, acceleration, state.velocity[0], state.position[0]
