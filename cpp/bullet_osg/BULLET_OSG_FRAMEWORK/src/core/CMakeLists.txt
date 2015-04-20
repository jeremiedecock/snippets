# Copyright (c) 2015 Jérémie DECOCK

set(core_src joint.h joint.cc 
             object.h object.cc 
             part.h part.cc
             bullet_environment.h bullet_environment.cc 
             osg_environment.h osg_environment.cc
)

add_library(core STATIC ${core_src})

