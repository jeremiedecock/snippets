# Copyright (c) 2015 Jérémie DECOCK

set(actuators_src motor.h  motor.cc
)

add_library(actuators STATIC ${actuators_src})
