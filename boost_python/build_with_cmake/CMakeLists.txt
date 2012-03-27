CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT(Python_Wrapper_Snippet)

#SET(CMAKE_CXX_COMPILER clang++)

# Find and setup boost.pthon for this project
#FIND_PACKAGE(boostpython REQUIRED)              # TODO

# CFLAGS
INCLUDE_DIRECTORIES(/usr/include/python2.7)      # TODO: improve this...
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC"  )
SET(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -fPIC"  )
SET(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fPIC"  )

# BUILD LIB
SET(python_wrapper_src func.cc python_wrapper.cc)
ADD_LIBRARY(cppfunc SHARED ${python_wrapper_src})

# LDFLAGS
#LINK_DIRECTORIES($ENV{BOOSTDIR}/stage/lib)      # TODO: improve this...
TARGET_LINK_LIBRARIES(cppfunc python2.7 boost_python)

