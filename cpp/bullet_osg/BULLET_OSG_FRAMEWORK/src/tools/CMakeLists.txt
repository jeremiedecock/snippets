# Copyright (c) 2015 Jérémie DECOCK

set(tools_src tools.h tools.cc
              part_logger_dat.h part_logger_dat.cc)

add_library(tools STATIC ${tools_src})
