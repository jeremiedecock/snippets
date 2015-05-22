# Copyright (c) 2015 Jérémie DECOCK

set(joint_slots_src hinge_slot.h  hinge_slot.cc
                    point_to_point_slot.h  point_to_point_slot.cc
                    fixed_slot.h  fixed_slot.cc
)

add_library(joint_slots STATIC ${joint_slots_src})
