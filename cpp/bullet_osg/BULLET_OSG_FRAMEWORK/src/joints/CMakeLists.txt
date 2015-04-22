# Copyright (c) 2015 Jérémie DECOCK

set(joints_src hinge.h  hinge.cc
               point_to_point.h  point_to_point.cc
)

add_library(joints STATIC ${joints_src})
