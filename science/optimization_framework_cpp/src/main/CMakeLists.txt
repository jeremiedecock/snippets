# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

### OPTIONS ###

OPTION(BUILD_TEST1 "Build test1 (a basic test)" OFF)

### COMMON TARGET_LINK_LIBRAIRIES ###

### ADD_EXECUTABLE ###

IF(BUILD_TEST1)
    ADD_EXECUTABLE(test1 test1.cpp)
    TARGET_LINK_LIBRARIES(test1 optimizer objective_function tools ${lib_boost_date_time} ${lib_boost_program_opt})
ENDIF(BUILD_TEST1)

