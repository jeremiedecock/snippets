# Copyright (c) 2015 Jérémie DECOCK

set(core_src actuator.h actuator.cc
             bullet_environment.h bullet_environment.cc 
             controller.h controller.cc
             joint.h joint.cc 
             object.h object.cc 
             osg_environment.h osg_environment.cc
             part.h part.cc
             sensor.h sensor.cc
)

add_library(core STATIC ${core_src})

