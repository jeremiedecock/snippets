# Copyright (c) 2015 Jérémie DECOCK

# To see which flags are actually uesd by Gcc/ld, type in a terminal:
# find <build-dir> -name "flags.make"   # CFLAGS
# find <build-dir> -name "link.txt"     # LDFLAGS

cmake_minimum_required(VERSION 2.6)

project(physics_framework)


## CONFIG #####################################################################

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR})
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)
set(CMAKE_BUILD_TYPE Debug)

# C++11 ###############################

# Taken from http://stackoverflow.com/questions/10851247/how-to-activate-c-11-in-cmake

include(CheckCXXCompilerFlag)
CHECK_CXX_COMPILER_FLAG("-std=c++11" COMPILER_SUPPORTS_CXX11)
CHECK_CXX_COMPILER_FLAG("-std=c++0x" COMPILER_SUPPORTS_CXX0X)

if(COMPILER_SUPPORTS_CXX11)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
elseif(COMPILER_SUPPORTS_CXX0X)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
else()
    message(STATUS "The compiler ${CMAKE_CXX_COMPILER} has no C++11 support. Please use a different C++ compiler.")
endif()


# OPTIONS #############################

# LLVM CLANG
option(USE_CLANG "Use LLVM Clang" OFF)
if(USE_CLANG)
    set(CMAKE_CXX_COMPILER clang++)
endif(USE_CLANG)

## STATIC COMPILATION (GNU only ?)
#option(USE_STATIC "Enable static compilation" OFF)
#if(USE_STATIC)
#    set(DBUILD_SHARED_LIBS OFF)
#    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static -static-libgcc -static-libstdc++"  )
#    set(Boost_USE_STATIC_LIBS ON)
#    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
#endif(USE_STATIC)

# GPROF (GNU only)
option(USE_GPROF "Enable gprof" OFF)
if(USE_GPROF)
    set(CMAKE_BUILD_TYPE Debug)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pg"  )
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pg"  )
endif(USE_GPROF)

# GCOV (GNU only)
option(USE_GCOV "Enable gcov" OFF)
if(USE_GCOV)
    set(CMAKE_BUILD_TYPE Debug)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage"  )
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage"  )
endif(USE_GCOV)

## NATIVE OPTIMIZATIONS (GCC ONLY)
#option(GCC_NATIVE "Optimize executable for modern hosts CPUs (GCC ONLY)" OFF)
#if(GCC_NATIVE)
#    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -march=native -mssse3" )
#    add_definitions(-DCMAKE_GCC_NATIVE)
#endif(GCC_NATIVE)
#
## EXPERIMENTAL OPTION
#option(USE_EXPERIMENTAL "Build experimental code" OFF)
#if(USE_EXPERIMENTAL)
#  add_definitions(-DEXPERIMENTAL)
#endif(USE_EXPERIMENTAL)


## BOOST ######################################################################

# See http://stackoverflow.com/questions/6646405/how-do-you-add-boost-libraries-in-cmakelists-txt

set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 

# Find and setup Boost for this project
find_package(Boost 1.55.0 COMPONENTS program_options)

# Boost includes
include_directories(${Boost_INCLUDE_DIRS})


## BULLET #####################################################################

# Find and setup Bullet for this project
find_package(Bullet)

# Bullet includes
include_directories(${BULLET_INCLUDE_DIRS})


## EIGEN ######################################################################

# Find and setup Eigen 3 for this project
find_package(Eigen3)

# Eigen 3 includes
include_directories(${EIGEN3_INCLUDE_DIR})


## OSG ########################################################################

# Find and setup OpenSceneGraph for this project
find_package(OpenSceneGraph 3.0.0 REQUIRED osgGA osgShadow osgViewer)

# OSG includes
include_directories(${OPENSCENEGRAPH_INCLUDE_DIRS})

# /usr/share/cmake-3.0/Modules/FindosgAnimation.cmake
# /usr/share/cmake-3.0/Modules/Findosg.cmake
# /usr/share/cmake-3.0/Modules/FindosgDB.cmake
# /usr/share/cmake-3.0/Modules/Findosg_functions.cmake
# /usr/share/cmake-3.0/Modules/FindosgFX.cmake
# /usr/share/cmake-3.0/Modules/FindosgGA.cmake
# /usr/share/cmake-3.0/Modules/FindosgIntrospection.cmake
# /usr/share/cmake-3.0/Modules/FindosgManipulator.cmake
# /usr/share/cmake-3.0/Modules/FindosgParticle.cmake
# /usr/share/cmake-3.0/Modules/FindosgPresentation.cmake
# /usr/share/cmake-3.0/Modules/FindosgProducer.cmake
# /usr/share/cmake-3.0/Modules/FindosgQt.cmake
# /usr/share/cmake-3.0/Modules/FindosgShadow.cmake
# /usr/share/cmake-3.0/Modules/FindosgSim.cmake
# /usr/share/cmake-3.0/Modules/FindosgTerrain.cmake
# /usr/share/cmake-3.0/Modules/FindosgText.cmake
# /usr/share/cmake-3.0/Modules/FindosgUtil.cmake
# /usr/share/cmake-3.0/Modules/FindosgViewer.cmake
# /usr/share/cmake-3.0/Modules/FindosgVolume.cmake
# /usr/share/cmake-3.0/Modules/FindosgWidget.cmake


## CFLAGS #####################################################################

message(STATUS "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}")
message(STATUS "CMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}")
message(STATUS "CMAKE_CXX_FLAGS_DEBUG=${CMAKE_CXX_FLAGS_DEBUG}")
message(STATUS "CMAKE_CXX_FLAGS_RELEASE=${CMAKE_CXX_FLAGS_RELEASE}")

include_directories(${PROJECT_SOURCE_DIR}/src ${PROJECT_SOURCE_DIR}/src/core ${PROJECT_SOURCE_DIR}/tests)


## SUB DIRECTORIES ############################################################

add_subdirectory(src)
#add_subdirectory(tests)
