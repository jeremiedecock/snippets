# Copyright (c) 2015 Jérémie DECOCK

set(sensors_src clock.h  clock.cc
)

add_library(sensors STATIC ${sensors_src})
