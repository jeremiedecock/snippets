# Copyright (c) 2015 Jérémie DECOCK

set(controllers_src constant_signal.h  constant_signal.cc
                    robudog_controller.h  robudog_controller.cc
                    sinusoidal_signal.h  sinusoidal_signal.cc
)

add_library(controllers STATIC ${controllers_src})
