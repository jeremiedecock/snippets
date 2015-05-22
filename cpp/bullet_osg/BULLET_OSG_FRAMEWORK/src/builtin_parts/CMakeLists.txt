# Copyright (c) 2015 Jérémie DECOCK

set(builtin_parts_src dynamixel_ax12.h  dynamixel_ax12.cc
                      robudog_trunk.h  robudog_trunk.cc
)

add_library(builtin_parts STATIC ${builtin_parts_src})
