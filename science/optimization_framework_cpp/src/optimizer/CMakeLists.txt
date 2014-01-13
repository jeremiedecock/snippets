# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

SET(optimizer_src optimizer.h   optimizer_naive.h
                  optimizer.cpp optimizer_naive.cpp)

ADD_LIBRARY(optimizer STATIC ${optimizer_src})

