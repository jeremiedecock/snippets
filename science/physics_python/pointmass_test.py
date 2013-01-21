#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013 Jérémie DECOCK (http://www.jdhp.org)

import sys
import os.path

from common.simulator import Simulator
from common.state import State

#from controllers import random_controller as controller_module
from kinematics.finite_difference_method import Kinematics
from models.pointmass_model import Model

def main():
    """Main function."""

    sys.path.append(os.path.abspath("."))

    # controller # model # kinematics # stop_condition # simulator

    state = State(1)
    model = Model()
    kinematics = Kinematics()

    simulator = Simulator(model, kinematics)

    simulator.run()


if __name__ == "__main__":
    main()
