# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

SET(optimizer_src optimizer.h   optimizer_naive.h   optimizer_gradient_descent.h
                  optimizer.cpp optimizer_naive.cpp optimizer_gradient_descent.cpp)

ADD_LIBRARY(optimizer STATIC ${optimizer_src})

