# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

SET(objective_function_src objective_function.h   sphere_function.h
                           objective_function.cpp sphere_function.cpp)

ADD_LIBRARY(objective_function STATIC ${objective_function_src})

