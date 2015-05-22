# Copyright (c) 2015 Jérémie DECOCK

set(builtin_objects_src robudog_jd.h  robudog_jd.cc
)

add_library(builtin_objects STATIC ${builtin_objects_src})
