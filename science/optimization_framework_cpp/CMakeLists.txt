# Copyright (c) 2014 Jérémie DECOCK <jd.jdhp@gmail.com>

# To see which flags are actually uesd by Gcc/ld, type in a terminal:
# find <build-dir> -name "flags.make"   # CFLAGS
# find <build-dir> -name "link.txt"     # LDFLAGS

CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(optimization_framework)

## CONFIG #####################################################################

SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})
SET(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
SET(CMAKE_BUILD_TYPE Debug)

# OPTIONS #############################

OPTION(USE_CLANG "Use LLVM Clang" OFF)
IF(USE_CLANG)
    SET(CMAKE_CXX_COMPILER clang++)
ENDIF(USE_CLANG)

# DETERMINISTIC_MODE
OPTION(USE_DETERMINISTIC_MODE "Enable Deterministic Mode" OFF)
IF(USE_DETERMINISTIC_MODE)
    ADD_DEFINITIONS(-DDETERMINISTIC_MODE)
ENDIF(USE_DETERMINISTIC_MODE)

# EXEC_VERBOSE
OPTION(EXEC_VERBOSE "Enable Exec Verbose Mode" OFF)
IF(EXEC_VERBOSE)
    ADD_DEFINITIONS(-DEXEC_VERBOSE)
ENDIF(EXEC_VERBOSE)
#SET(EXEC_VERBOSE_LEVEL "0" CACHE STRING "Verbose Level")
#ADD_DEFINITIONS(-DEXEC_VERBOSE_LEVEL=${EXEC_VERBOSE_LEVEL})

# OPENMP (GNU only)
OPTION(USE_OPENMP "Enable OpenMP" OFF)
IF(USE_OPENMP)
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp"  )
ENDIF(USE_OPENMP)

# STATIC COMPILATION (GNU only ?)
OPTION(USE_STATIC "Enable static compilation" OFF)
IF(USE_STATIC)
    SET(DBUILD_SHARED_LIBS OFF)
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static"  )
    SET(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
ENDIF(USE_STATIC)

# GPROF (GNU only)
OPTION(USE_GPROF "Enable gprof" OFF)
IF(USE_GPROF)
    SET(CMAKE_BUILD_TYPE Debug)
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pg"  )
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pg"  )
ENDIF(USE_GPROF)

# GCOV (GNU only)
OPTION(USE_GCOV "Enable gcov" OFF)
IF(USE_GCOV)
    SET(CMAKE_BUILD_TYPE Debug)
	SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage"  )
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage"  )
ENDIF(USE_GCOV)

# NATIVE OPTIMIZATIONS
OPTION(GCC_NATIVE "Optimize executable for modern hosts CPUs (GCC ONLY)" OFF)
IF(GCC_NATIVE)
	SET(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native -mssse3" )
ENDIF(GCC_NATIVE)

## LIBS #######################################################################

# BOOST
IF(WIN32)
    # WIN32
    SET(lib_boost_date_time   "boost_date_time-vc100-mt-1_47")
    SET(lib_boost_program_opt "libboost_program_options-vc100-mt-1_47")
    SET(lib_boost_python      "boost_python-vc100-mt-1_47")
ELSE(WIN32)
    # LINUX
    SET(BOOST_INCLUDE_PATH    $ENV{BOOSTDIR})
    SET(BOOST_LINK_PATH       $ENV{BOOSTDIR}/stage/lib)
    SET(lib_boost_date_time   "boost_date_time")
	SET(lib_boost_program_opt "boost_program_options")
    SET(lib_boost_python      "boost_python")
ENDIF(WIN32)

INCLUDE_DIRECTORIES(${BOOST_INCLUDE_PATH})
LINK_DIRECTORIES(${BOOST_LINK_PATH})

## SRC ########################################################################

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/src ${PROJECT_SOURCE_DIR}/src/optimizer ${PROJECT_SOURCE_DIR}/src/objective_function) #${PROJECT_SOURCE_DIR}/tests)

ADD_SUBDIRECTORY(src)
#ADD_SUBDIRECTORY(tests)
