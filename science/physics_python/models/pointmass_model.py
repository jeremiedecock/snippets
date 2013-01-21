# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)


class Model:

    def __init__(self, mass=1, gravity=9.6):
        self.mass = mass
        self.gravity = gravity


    def compute_acceleration(self, state):

        # F = m.g
        total_external_force = self.mass * self.gravity

        # a = f/m
        acceleration = total_external_force / self.mass

        return acceleration

