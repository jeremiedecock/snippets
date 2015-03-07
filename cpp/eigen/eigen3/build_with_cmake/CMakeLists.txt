cmake_minimum_required(VERSION 2.6)

project(eigen3_cmake_hello)

# Find and setup Eigen 3 for this project
find_package(Eigen3)

# Tell CMake to create the helloworld executable
add_executable(hello hello.cc)

# Eigen 3 includes
include_directories(${EIGEN3_INCLUDE_DIR})
