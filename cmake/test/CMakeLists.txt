CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(test)

# OPTIONS #############################

OPTION(USE_STATIC "Enable static compilation" OFF)

#SET(CMAKE_CXX_COMPILER clang++)

## CFLAGS #####################################################################

MESSAGE(STATUS "CMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}")
MESSAGE(STATUS "CMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}")
MESSAGE(STATUS "CMAKE_CXX_FLAGS_DEBUG=${CMAKE_CXX_FLAGS_DEBUG}")
MESSAGE(STATUS "CMAKE_CXX_FLAGS_RELEASE=${CMAKE_CXX_FLAGS_RELEASE}")

## LIBS #######################################################################

# STATIC
# TODO : GNU only ?
IF(USE_STATIC)
    SET(DBUILD_SHARED_LIBS OFF)
    SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static"  )
ENDIF(USE_STATIC)

## SRC ########################################################################

# TODO ?
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/src)
ADD_SUBDIRECTORY(src)
