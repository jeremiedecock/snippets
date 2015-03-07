cmake_minimum_required(VERSION 2.6)

project(hello_snippet)

# Find and setup OpenSceneGraph for this project
find_package(OpenSceneGraph 3.0.0 REQUIRED osgShadow osgViewer)

# OSG includes
include_directories(${OPENSCENEGRAPH_INCLUDE_DIRS})

# Executable
add_executable(hello hello.cc)

# OSG libs
target_link_libraries(hello ${OPENSCENEGRAPH_LIBRARIES})
