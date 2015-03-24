# Copyright (c) 2015 Jérémie DECOCK

set(tools_src tools.h tools.cc
              logger_time_steps_parts_dat.h  logger_time_steps_parts_dat.cc
              logger_time_steps_parts_json.h logger_time_steps_parts_json.cc
              logger_ticks_parts_dat.h  logger_ticks_parts_dat.cc
              logger_ticks_parts_json.h logger_ticks_parts_json.cc)

add_library(tools STATIC ${tools_src})
