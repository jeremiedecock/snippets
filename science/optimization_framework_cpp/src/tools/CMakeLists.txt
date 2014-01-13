# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

SET(tools_src utils.cpp random_number_generator.cpp
              utils.h   random_number_generator.h)

ADD_LIBRARY(tools STATIC ${tools_src})
