# Copyright (c) 2015 Jérémie DECOCK

set(parts_src box.h  box.cc
              ground.h ground.cc
              sphere.h sphere.cc
)

add_library(parts STATIC ${parts_src})
